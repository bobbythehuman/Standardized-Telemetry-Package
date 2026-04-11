import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_structures.BNG_struct import MetaData
from support.server import telemetryManager


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("PacketCData")
            if telemetry:
                packetSpeed = telemetry.speed
                speedValue = round(packetSpeed * 3.6, 2)

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayGear(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("PacketCData")
            if telemetry:
                gearValue = telemetry.gears

                print(f"Gear: {gearValue}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


# the IP of the PS5
sourceIP = "192.168.1.1"

activeThreads = telemetryManager()
activeThreads.updateMeta(MetaData)
# add the source IP of the PS5
activeThreads.updateSendIP(sourceIP)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayGear)
activeThreads.StartTelemetry()
