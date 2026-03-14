import socket
from dataclasses import dataclass
import threading
from typing import Generator, Tuple, Type, Any, Optional

from support.digestion import dynamic_ingest

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


class threadManager:
    def __init__(self):
        self.ACTIVE_META = None
        self.IP = None

        self.activeStorage = None
        self.readOnlyStorage = None
        self.stop_event = threading.Event()

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
            kwargs={"MetaData": self.ACTIVE_META, "IP": self.IP, "storage": self.activeStorage, "stop_event": self.stop_event},
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

    def stopThreads(self):
        if not self.workersAreWorking:
            return
        if not self.networkThread:
            return

        self.stop_event.set()
        self.networkThread.join(timeout=0.5)

        for workerName, workerThread in self.workerThreads.items():
            workerThread.join(timeout=0.5)
            if workerThread.is_alive():
                print(f"[MAIN] [WARNING]\tWarning: {workerName} did not stop in time.")

        self.workersAreWorking = False
        print("\n[MAIN] [INFO]\tAll threads stopped. Exiting.")


# ---------------------------------------------------------------------------
# Misc Utility Functions
# ---------------------------------------------------------------------------


def construct_packet(data: bytes, packetID: int, packetInfo) -> type | None:
    structureMatch = False
    packet = None

    # the loop is for cases where there are multiple possible packet structures for a given packet ID, which is the case for packet 8 in PC2
    for packetBufferSize, packetStruct in packetInfo:
        if len(data) < packetBufferSize:
            print(f"[Warning]\tReceived data length {len(data)} is less than expected packet buffer size {packetBufferSize} for packet ID {packetID}")
            # raise ValueError(f"Received data length {len(data)} is less than expected packet buffer size {packetBufferSize}")
        elif len(data) > packetBufferSize:
            print(
                f"[Warning]\tReceived data length {len(data)} is greater than expected packet buffer size {packetBufferSize} for packet ID {packetID}. Extra data will be ignored."
            )
            # raise ValueError(f"Received data length {len(data)} is greater than expected packet buffer size {packetBufferSize}")
        try:
            rawPacket = packetStruct.from_buffer_copy(data[0:packetBufferSize])
        except ValueError as exc:
            raise ValueError(f"[Error]\tFailed to construct packet {packetStruct.__name__}: {exc}")
            # continue
        else:
            packet = dynamic_ingest(rawPacket)
            structureMatch = True
            break

    if not structureMatch:
        print(f"[Error]\tNo matching structure found for packet ID {packetID} with data length {len(data)}")
        packet = None

    return packet


# ---------------------------------------------------------------------------
# Thread 1 — Network Listener
# ---------------------------------------------------------------------------


def get_telemetry(
    MetaData: Type, IP: str = "0.0.0.0", stop_event: Optional[threading.Event] = None
) -> Generator[Tuple[Type[Any] | None, int, Type[Any]], None, None]:

    UDP_IP = IP
    UDP_PORT = MetaData.port

    _fullBufferSize = MetaData.fullBufferSize
    _headerBufferSize = MetaData.headerInfo[0]
    _headerPacketStruct = MetaData.headerInfo[1]
    _packetIDName = MetaData.packetIDAttribute

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0)  # allows checking stop_event periodically
    sock.bind((UDP_IP, UDP_PORT))

    print(f"[NTWK] [Info]\tServer started on {UDP_IP}:{UDP_PORT}")

    if not stop_event:
        print("[NTWK] [Warning]\tNo stop event provided, running indefinitely. Use Ctrl+C to stop.")
        while True:
            try:
                data, _ = sock.recvfrom(_fullBufferSize)
            except KeyboardInterrupt:
                print("[NTWK] [Info]\tKeyboardInterrupt received, shutting down server.")
                break

            rawHeaderPacket = _headerPacketStruct.from_buffer_copy(data[0:_headerBufferSize])
            headerPacket = dynamic_ingest(rawHeaderPacket)

            packetID = int(getattr(headerPacket, _packetIDName))
            packetInfo = MetaData.packetInfo.get(packetID)

            if packetInfo:
                packet = construct_packet(data, packetID, packetInfo)
            else:
                print("ID not found")
                packet = None

            yield packet, packetID, headerPacket
    else:
        # only run if stop_event is provided, allowing for graceful shutdown
        print("[NTWK] [Info]\tStop event provided, running until stop_event is set.")
        while not stop_event.is_set():
            try:
                data, _ = sock.recvfrom(_fullBufferSize)
            except TimeoutError:
                continue
            except KeyboardInterrupt:
                print("[NTWK] [Info]\tKeyboardInterrupt received, shutting down server.")
                stop_event.set()
                break
            except OSError as exc:
                print(f"[NTWK] [Error]\tSocket error: {exc}")
                stop_event.set()
                break

            rawHeaderPacket = _headerPacketStruct.from_buffer_copy(data[0:_headerBufferSize])
            headerPacket = dynamic_ingest(rawHeaderPacket)

            packetID = int(getattr(headerPacket, _packetIDName))
            packetInfo = MetaData.packetInfo.get(packetID)

            if packetInfo:
                packet = construct_packet(data, packetID, packetInfo)
            else:
                print("ID not found")
                packet = None

            yield packet, packetID, headerPacket
    print("[NTWK] [Info]\tServer shutting down.")


def network_listener(MetaData: Type, storage: CentralStorage, IP: str = "0.0.0.0", stop_event: Optional[threading.Event] = None) -> None:
    if storage is None:
        raise ValueError("[NTWK] [Error]\tCentralStorage instance must be provided to network_listener")
    a = 1
    for packet, packetID, headerPacket in get_telemetry(MetaData, IP, stop_event):
        a += 1
        # print(f"[NTWK] [Info]\tReceived packet ID {packetID}")
        storage._write(packetID, packet)
