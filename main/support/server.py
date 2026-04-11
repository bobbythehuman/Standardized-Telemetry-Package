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


class telemetryManager:
    def __init__(self):
        self.ACTIVE_METADATA = None
        self.IP = "0.0.0.0"
        self.destinationIP = None

        self.activeStorage = None
        self.readOnlyStorage = None
        self.stop_event = threading.Event()
        self.manuallyStopped = False

        self.networkThread = None
        self.workerThreads: dict[int, threading.Thread] = {}

        self.workersAreWorking = False
        self.threadCount = 0
        self.multiThreaded = True

    # User controlled functions

    def updateMeta(self, MetaData):
        if self.ACTIVE_METADATA != MetaData:
            self.ACTIVE_METADATA = MetaData
            self.activeStorage = CentralStorage(self.ACTIVE_METADATA)
            self.readOnlyStorage = ReadOnlyStorage(self.activeStorage)
        self.unpackMetaData()

    def updateLocalIP(self, ip: str):
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

    def manualStop(self, target: bool):
        """Manually stop the program by entering q to stop"""
        self.manuallyStopped = target

    def isMultiThreaded(self, target: bool):
        self.multiThreaded = target

    # Misc packet functions

    def metaDataCheck(self, name: str, value: Any = None):
        if hasattr(self.ACTIVE_METADATA, name):
            return getattr(self.ACTIVE_METADATA, name)
            # _heartBeatPort = self.ACTIVE_METADATA.value
        else:
            return value
            # _heartBeatPort = None

    def unpackMetaData(self):
        self.mainPort = self.metaDataCheck("port")
        self.fullBufferSize = self.metaDataCheck("fullBufferSize")

        self.heartBeatPort = self.metaDataCheck("heartBeatPort")
        self.heartBeatFunc = self.metaDataCheck("heartBeatFunc")

        self.handShakePort = self.metaDataCheck("handShakePort")
        self.handShakeFunc = self.metaDataCheck("handShakeFunc")

        self.decryptionFunc = self.metaDataCheck("decrytionFunc")

        self.headerBufferSize = self.metaDataCheck("headerInfo")[0]
        self.headerPacketStruct = self.metaDataCheck("headerInfo")[1]
        self.packetIDAttr = self.metaDataCheck("packetIDAttribute")

        self.packetInfo = self.metaDataCheck("packetInfo", [])

    # Misc thread function

    def wait(self, time: float):
        self.stop_event.wait(time)

    def triggerStop(self):
        if self.stop_event:
            self.stop_event.set()
        self.manuallyStopped = True

    def isStillActive(self) -> bool:
        return self.stop_event.is_set() or self.manuallyStopped

    # Start and Stop functions

    def startThreads(self) -> None:
        if not self.ACTIVE_METADATA:
            return
        if not self.IP:
            return

        self.networkThread = threading.Thread(
            target=self.network_listener,
            kwargs={},
            daemon=True,
        )

        self.networkThread.start()

        for workerName, workerThread in self.workerThreads.items():
            workerThread.start()

        self.workersAreWorking = True

    def waitForStopSignal(self):
        endProgram = ""
        try:
            while not self.isStillActive():
                self.wait(0.5)

                if self.manuallyStopped:
                    # only stop threads here if they dont get stopped any where else
                    endProgram = input(f"[Q] to quit the program: ")
                    if endProgram.lower() == "q":
                        self.triggerStop()

        except KeyboardInterrupt:
            print("\n[MAIN] [INFO]\tKeyboardInterrupt received.")
        finally:
            print("[MAIN] [INFO]\tStopping all threads\n")
            self.stopThreads()

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
        # comment lines below to make a manual stop outside class
        self.waitForStopSignal()
        print("[MAIN] [INFO]\tEnd at ", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

    # Misc packet function

    def construct_packet(self, data: bytes, possiblePacketStruct: Tuple) -> type | None:
        packet = None
        packetSizes = []
        dataLength = len(data)
        for packetBufferSize, packetStruct in possiblePacketStruct:
            if packetBufferSize != dataLength:
                packetSizes.append(packetBufferSize)
            else:
                try:
                    rawPacket = packetStruct.from_buffer_copy(data[0:packetBufferSize])
                except ValueError as exc:
                    continue
                else:
                    packet = dynamic_ingest(rawPacket)
                    break
        if len(self.packetInfo) == len(packetSizes):
            print(f"[Warning]\tNo matching packet buffer size [{packetSizes}] for data length {dataLength}")
            packet = None
        return packet

    def retrieve_packet(self, data: bytes) -> tuple[type | None, int, Any]:
        if self.headerPacketStruct:
            rawHeaderPacket = self.headerPacketStruct.from_buffer_copy(data[0 : self.headerBufferSize])
            headerPacket = dynamic_ingest(rawHeaderPacket)

            packetID = int(getattr(headerPacket, self.packetIDAttr))
        else:
            headerPacket = None
            packetID = 0

        possiblePacketStruct = self.packetInfo.get(packetID)
        if possiblePacketStruct:
            packet = self.construct_packet(data, possiblePacketStruct)
        else:
            print("ID not found")
            packet = None

        return packet, packetID, headerPacket

    # Main packet function

    def process_loop(self, sock, PACKET_COUNTER):
        HEARTBEAT_INTERVAL = 5
        packet = None
        packetID = 0
        headerPacket = None
        heartBeatDestination = (self.destinationIP, self.heartBeatPort)

        if self.heartBeatFunc:
            if PACKET_COUNTER % HEARTBEAT_INTERVAL == 0:
                self.heartBeatFunc(sock, heartBeatDestination)
                PACKET_COUNTER += 1
            else:
                PACKET_COUNTER = 0

        try:
            data, _ = sock.recvfrom(self.fullBufferSize)
        except TimeoutError:
            if self.heartBeatFunc:
                self.heartBeatFunc(sock, heartBeatDestination)
                PACKET_COUNTER = 0
            # continue
        except KeyboardInterrupt:
            print("[NTWK] [Info]\tKeyboardInterrupt received, shutting down server.")
            self.triggerStop()
            # continue
        except OSError as exc:
            print(f"[NTWK] [Error]\tSocket error: {exc}")
            self.triggerStop()
            # continue
        else:
            if self.decryptionFunc:
                data = self.decryptionFunc(data)

            packet, packetID, headerPacket = self.retrieve_packet(data)
        return packet, packetID, headerPacket

    def get_telemetry(self) -> Generator[Tuple[Type[Any] | None, int, Type[Any] | None], None, None]:
        UDP_IP = self.IP
        UDP_PORT = self.mainPort
        # HEARTBEAT_INTERVAL = 5
        PACKET_COUNTER = 0

        handShakeDestination = (self.destinationIP, self.handShakePort)

        if (self.handShakeFunc or self.heartBeatFunc) and not self.destinationIP:
            raise ValueError("[NTWK] [Error]\tDestination IP must be set for handshakes or heartbeats.")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # listen to occupied ports
        sock.settimeout(1.0)  # allows checking stop_event periodically
        sock.bind((UDP_IP, UDP_PORT))

        print(f"[NTWK] [Info]\tServer started on {UDP_IP}:{UDP_PORT}")

        if self.handShakeFunc:
            self.handShakeFunc[0](sock, handShakeDestination)

        print("[NTWK] [Info]\tStop event provided, running until stop_event is set.")
        while not self.isStillActive():
            yield self.process_loop(sock, PACKET_COUNTER)

        if self.handShakeFunc:
            self.handShakeFunc[1](sock, handShakeDestination)
        sock.close()
        print("[NTWK] [Info]\tServer shutting down.")

    def network_listener(self) -> None:
        if self.activeStorage is None:
            raise ValueError("[NTWK] [Error]\tCentralStorage instance must be provided to network_listener")

        for packet, packetID, headerPacket in self.get_telemetry():
            # print(f"[NTWK] [Info]\tReceived packet ID {packetID}")
            self.activeStorage._write(packetID, packet)
