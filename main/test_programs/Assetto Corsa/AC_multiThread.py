import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data_structures.AC_struct import MetaData
from support.server import telemetryManager


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("RTCarData")

            if telemetry:
                packetSpeed = telemetry.speed_Mph
                speedValue = round(packetSpeed, 2)
                print(f"{speedValue} MPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayLap(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            lapData = data.get("RTLapData")
            if lapData:
                lap = lapData.lap
                print(f"Lap: {lap}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


sourceIP = "127.0.0.1"

activeThreads = telemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.updateSendIP(sourceIP)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayLap)
activeThreads.StartTelemetry()
