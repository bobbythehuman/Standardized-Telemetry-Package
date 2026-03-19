import socket
import threading
from dataclasses import dataclass
from typing import Generator, Tuple, Type, Any, Optional
from datetime import datetime

from support.digestion import dynamic_ingest

# from ..support.digestion import dynamic_ingest

# ---------------------------------------------------------------------------
# Central Storage
# ---------------------------------------------------------------------------


@dataclass
class CentralStorage:
    """
    Holds the latest network data.  Worker threads receive a read-only view
    via ReadOnlyStorage so they cannot accidentally mutate the contents.
    """

    def __init__(self, MetaData) -> None:
        self._lock = threading.RLock()

        self.allData = {}
        self.lastestData = {}

        packetNames = MetaData.packetInfo.items()
        for packetID, packetInfo in packetNames:
            for packetBufferSize, packetStruct in packetInfo:
                packetName = packetStruct.__name__
                if packetName not in self.allData:
                    self.allData[packetName] = []
                    self.lastestData[packetName] = None

    def _write(self, packetID: int, data) -> None:
        """Called only by the network thread."""
        with self._lock:
            if data:
                packetName = data.__name__

                self.allData[packetName].append(data)
                self.lastestData[packetName] = data

    def snapshot(self) -> dict[str, Any]:
        """Return a consistent, immutable snapshot for worker threads."""
        with self._lock:
            return {
                "allData": self.allData.copy(),
                "lastestData": self.lastestData.copy(),
            }


class ReadOnlyStorage:
    """
    Thin wrapper passed to worker threads.
    Exposes only .snapshot() — no write methods visible.
    """

    def __init__(self, storage: CentralStorage) -> None:
        self._storage = storage

    def snapshot(self) -> dict[str, Any]:
        return self._storage.snapshot()


# ---------------------------------------------------------------------------
# Manages Threads
# ---------------------------------------------------------------------------


class multiThreadedTelemetry:
    def __init__(self):
        self.ACTIVE_META = None
        self.IP = "0.0.0.0"
        self.destinationIP = None

        self.activeStorage = None
        self.readOnlyStorage = None
        self.stop_event = threading.Event()
        self.manuallyStop = False

        self.networkThread = None
        self.workerThreads: dict[int, threading.Thread] = {}

        self.workersAreWorking = False
        self.threadCount = 0

    def updateMeta(self, MetaData):
        if self.ACTIVE_META != MetaData:
            self.ACTIVE_META = MetaData
            self.activeStorage = CentralStorage(self.ACTIVE_META)
            self.readOnlyStorage = ReadOnlyStorage(self.activeStorage)

    def updateIP(self, ip: str):
        self.IP = ip

    def updateSendIP(self, ip: str):
        self.destinationIP = ip

    def addWorkerThread(self, mainFunc):
        self.threadCount += 1
        # readOnlyStorage may need updating when metadata gets updated
        workerThread = threading.Thread(
            target=mainFunc,
            kwargs={"worker_id": self.threadCount, "ro_storage": self.readOnlyStorage, "stop_event": self.stop_event},
            daemon=True,
        )
        self.workerThreads.update({self.threadCount: workerThread})

    def startThreads(self) -> None:
        if not self.ACTIVE_META:
            return
        if not self.IP:
            return

        self.networkThread = threading.Thread(
            target=network_listener,
            kwargs={
                "MetaData": self.ACTIVE_META,
                "IP": self.IP,
                "storage": self.activeStorage,
                "stop_event": self.stop_event,
                "destinationIP": self.destinationIP,
            },
            daemon=True,
        )

        self.networkThread.start()

        for workerName, workerThread in self.workerThreads.items():
            workerThread.start()

        self.workersAreWorking = True

    def isStillActive(self) -> bool:
        return self.stop_event.is_set()

    def wait(self, time: float):
        self.stop_event.wait(time)

    def triggerStop(self):
        self.stop_event.set()

    def manualStop(self, target):
        self.manuallyStop = target

    def stopThreads(self):
        if not self.workersAreWorking:
            return
        if not self.networkThread:
            return

        self.triggerStop()
        self.networkThread.join(timeout=0.5)

        for workerName, workerThread in self.workerThreads.items():
            workerThread.join(timeout=0.5)
            if workerThread.is_alive():
                print(f"[MAIN] [WARNING]\tWarning: {workerName} did not stop in time.")

        self.workersAreWorking = False
        print("\n[MAIN] [INFO]\tAll threads stopped. Exiting.")

    def StartTelemetry(self):
        print("[MAIN] [INFO]\tStart at ", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))
        self.startThreads()
        print("\n[MAIN] [INFO]\tRunning — press Ctrl+C to stop.")
        self.waitForStopSignal()
        print("[MAIN] [INFO]\tEnd at ", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

    def waitForStopSignal(self):
        endProgram = ""
        try:
            while not self.isStillActive():
                self.wait(0.5)

                if self.manuallyStop:
                    # only stop threads here if they dont get stopped any where else
                    endProgram = input(f"[Q] to quit the program: ")
                    if endProgram.lower() == "q":
                        self.triggerStop()

        except KeyboardInterrupt:
            print("\n[MAIN] [INFO]\tKeyboardInterrupt received.")
        finally:
            print("[MAIN] [INFO]\tStopping all threads\n")
            self.stopThreads()


# ---------------------------------------------------------------------------
# Misc Utility Functions
# ---------------------------------------------------------------------------


def construct_packet(data: bytes, packetID: int, packetInfo) -> type | None:
    structureMatch = False
    packet = None

    # the loop is for cases where there are multiple possible packet structures
    packetSizes = []
    dataLength = len(data)
    for packetBufferSize, packetStruct in packetInfo:

        if packetBufferSize != dataLength:
            # print(
            #     f"[Warning]\tReceived data length {dataLength} doesnt match expected packet buffer size {packetBufferSize} for packet ID {packetID}"
            # )
            packetSizes.append(packetBufferSize)

        else:
            try:
                rawPacket = packetStruct.from_buffer_copy(data[0:packetBufferSize])
            except ValueError as exc:
                continue
            else:
                # check and do cipher here
                packet = dynamic_ingest(rawPacket)
                structureMatch = True
                break

    if len(packetInfo) == len(packetSizes):
        print(f"[Warning]\tNo matching packet buffer size [{packetSizes}] for data length {dataLength}")
        packet = None

    if not structureMatch:
        print(f"[Error]\tNo matching structure found for packet ID {packetID} with data length {len(data)}")
        packet = None

    return packet


def retrieve_packet(data: bytes, MetaData) -> tuple[type | None, int, Any]:
    _headerPacketStruct = MetaData.headerInfo[1]

    if _headerPacketStruct:
        _headerBufferSize = MetaData.headerInfo[0]
        _packetIDName = MetaData.packetIDAttribute

        rawHeaderPacket = _headerPacketStruct.from_buffer_copy(data[0:_headerBufferSize])
        headerPacket = dynamic_ingest(rawHeaderPacket)

        packetID = int(getattr(headerPacket, _packetIDName))
    else:
        headerPacket = None
        packetID = 0

    packetInfo = MetaData.packetInfo.get(packetID)

    if packetInfo:
        packet = construct_packet(data, packetID, packetInfo)
    else:
        print("ID not found")
        packet = None

    return packet, packetID, headerPacket


# ---------------------------------------------------------------------------
# Thread 1 — Network Listener
# ---------------------------------------------------------------------------


def get_telemetry(
    MetaData: Type, IP: str = "0.0.0.0", stop_event: Optional[threading.Event] = None, destinationIP=None
) -> Generator[Tuple[Type[Any] | None, int, Type[Any] | None], None, None]:

    UDP_IP = IP
    UDP_PORT = MetaData.port
    manuallyStopped = False

    _fullBufferSize = MetaData.fullBufferSize
    _headerBufferSize = MetaData.headerInfo[0]
    _headerPacketStruct = MetaData.headerInfo[1]
    _packetIDName = MetaData.packetIDAttribute

    # if the game requires a heart beat
    if hasattr(MetaData, "heartBeatFunc"):
        heartBeat = MetaData.heartBeatFunc
    else:
        heartBeat = None

    if hasattr(MetaData, "destinationPort"):
        _destinationPort = MetaData.destinationPort
    else:
        _destinationPort = None

    HEARTBEAT_INTERVAL = 5
    PACKET_COUNTER = 0
    if heartBeat and not destinationIP:
        raise Exception(f"Heart beat is present, but no destination IP was provided!")

    # if the game data requires decrytion/ de-ciphering
    if hasattr(MetaData, "decrytionFunc"):
        _decryptionAlgorithm = MetaData.decrytionFunc
    else:
        _decryptionAlgorithm = None

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0)  # allows checking stop_event periodically
    sock.bind((UDP_IP, UDP_PORT))

    print(f"[NTWK] [Info]\tServer started on {UDP_IP}:{UDP_PORT}")

    if not stop_event:
        # * Method 1
        # no stop_event avaiable, probably running single threaded
        # TODO an error occours when trying to stop with keyboardInterrupt
        print("[NTWK] [Warning]\tNo stop event provided, running indefinitely. Use Ctrl+C to stop.")
        while not manuallyStopped:
            if heartBeat:
                if PACKET_COUNTER % HEARTBEAT_INTERVAL == 0:
                    heartBeat(sock, (destinationIP, _destinationPort))
                    PACKET_COUNTER += 1
                else:
                    PACKET_COUNTER = 0

            try:
                data, _ = sock.recvfrom(_fullBufferSize)
            except TimeoutError:
                if heartBeat:
                    heartBeat(sock, (destinationIP, _destinationPort))
                    PACKET_COUNTER = 0
                # continue
            except KeyboardInterrupt:
                print("[NTWK] [Info]\tKeyboardInterrupt received, shutting down server.")
                manuallyStopped = True
                # continue
            except OSError as exc:
                print(f"[NTWK] [Error]\tSocket error: {exc}")
                manuallyStopped = True
                # continue
            else:
                if _decryptionAlgorithm:
                    data = _decryptionAlgorithm(data)

                packet, packetID, headerPacket = retrieve_packet(data, MetaData)

                yield packet, packetID, headerPacket
    else:
        # * Method 2
        # only run if stop_event is provided
        print("[NTWK] [Info]\tStop event provided, running until stop_event is set.")
        while not stop_event.is_set():
            if heartBeat:
                if PACKET_COUNTER % HEARTBEAT_INTERVAL == 0:
                    heartBeat(sock, (destinationIP, _destinationPort))
                    PACKET_COUNTER += 1
                else:
                    PACKET_COUNTER = 0

            try:
                data, _ = sock.recvfrom(_fullBufferSize)
            except TimeoutError:
                if heartBeat:
                    heartBeat(sock, (destinationIP, _destinationPort))
                    PACKET_COUNTER = 0
                # continue
            except KeyboardInterrupt:
                print("[NTWK] [Info]\tKeyboardInterrupt received, shutting down server.")
                stop_event.set()
                # continue
            except OSError as exc:
                print(f"[NTWK] [Error]\tSocket error: {exc}")
                stop_event.set()
                # continue
            else:
                if _decryptionAlgorithm:
                    data = _decryptionAlgorithm(data)

                packet, packetID, headerPacket = retrieve_packet(data, MetaData)

                yield packet, packetID, headerPacket

    sock.close()
    print("[NTWK] [Info]\tServer shutting down.")


def network_listener(
    MetaData: Type, storage: CentralStorage, IP: str = "0.0.0.0", stop_event: Optional[threading.Event] = None, destinationIP=None
) -> None:
    if storage is None:
        raise ValueError("[NTWK] [Error]\tCentralStorage instance must be provided to network_listener")
    # a = 1
    for packet, packetID, headerPacket in get_telemetry(MetaData, IP, stop_event, destinationIP=destinationIP):
        # a += 1
        # print(f"[NTWK] [Info]\tReceived packet ID {packetID}")
        storage._write(packetID, packet)
