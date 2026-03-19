import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_structures.f1_2024_struct import MetaData
from support.server import multiThreadedTelemetry


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("PacketCarTelemetryData")
            if telemetry:
                currnetPlayer = telemetry.m_carTelemetryData[0]
                speedValue = currnetPlayer.m_speed

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayCurrentLap(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            lapData = data.get("PacketLapData")
            if lapData:
                currnetPlayer = lapData.m_lapData[0]
                currentLap = currnetPlayer.m_currentLapNum

                print(f"Lap {currentLap}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = multiThreadedTelemetry()
activeThreads.updateMeta(MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayCurrentLap)
activeThreads.StartTelemetry()
