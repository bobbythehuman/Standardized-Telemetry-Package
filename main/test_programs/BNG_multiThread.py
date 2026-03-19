import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_structures.BNG_struct import MetaData
from support.server import multiThreadedTelemetry


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("TelemetryData")
            if telemetry:
                packetSpeed = telemetry.speed
                speedValue = round(packetSpeed * 3.6, 2)

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayFormat(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            motionData = data.get("MotionSim")
            if motionData:
                format = motionData.format

                print(f"Format: {format}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = multiThreadedTelemetry()
activeThreads.updateMeta(MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayFormat)
activeThreads.StartTelemetry()
