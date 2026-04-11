"""
Architecture:
    - Main thread   : creates storage, starts threads, waits for stop signal
    - Thread 1      : network listener — receives UDP data, decodes, writes to storage
    - Thread 2+     : user-defined worker threads with read-only access to storage
"""

# TODO
# do readme
# auto find files from data_structure folder then retreive metaData class
# create a folder for worker functions

import time
import threading

from support.server import ReadOnlyStorage, telemetryManager

from data_structures.F1_2024_struct import MetaData as F12024MetaData
from data_structures.BNG_struct import MetaData as BNGMetaData
from data_structures.PC2_struct import MetaData as PC2MetaData
from data_structures.FH4_struct import MetaData as FH4MetaData
from data_structures.FH5_struct import MetaData as FH5MetaData
from data_structures.FM7_struct import MetaData as FM7MetaData
from data_structures.FM8_struct import MetaData as FM8MetaData
from data_structures.AC_struct import MetaData as ACMetaData

# from data_structures.GT7_struct import MetaData as GT7MetaData


def example_worker_thread(worker_id: int, ro_storage: ReadOnlyStorage, stop_event: threading.Event) -> None:
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()
        # -----------------------------------------------
        # do something here
        # -----------------------------------------------

        time.sleep(0.2)
        # * demo - stopping within thread
        # a = input("enter [a]: ")
        # if a == "a":
        #     stop_event.set()

        # * demo - printing your current speed in f1 24
        # data = snapshot.get("lastestData")
        # if data:
        #     telemetry = data.get("PacketCarTelemetryData")
        #     if telemetry:
        #         speed = telemetry.m_carTelemetryData[0].m_speed
        #         print(speed)

        # * demo - printing your current speed in beamng
        # data = snapshot.get("lastestData")
        # if data:
        #     telemetry = data.get("TelemetryData")
        #     if telemetry:
        #         speed = telemetry.speed
        #         roundedSpeed = round(speed * 2.23694, 2)
        #         gear = telemetry.gear if telemetry.gear else "\x00"
        #         print(f"{ord(gear)-1} : {roundedSpeed}")

        # * demo - printing your current speed in project cars 2
        # data = snapshot.get("lastestData")
        # if data:
        #     telemetry = data.get("TelemetryData")
        #     if telemetry:
        #         speed = telemetry.sSpeed
        #         print(round(speed * 2.23694, 2))

        # * demo - printing your current speed in forza motorsports 8
        # data = snapshot.get("lastestData")
        # if data:
        #     telemetry = data.get("SledData")
        #     if telemetry:
        #         engRPM = telemetry.CurrentEngineRpm
        #         print(engRPM)
        #     telemetry = data.get("DashData")
        #     if telemetry:
        #         speed = telemetry.Speed
        #         print(round(speed * 2.23694, 2))

        # * demo - printing your current speed in gran turismo 7
        # data = snapshot.get("lastestData")
        # if data:
        #     telemetry = data.get("PacketCData")
        #     if telemetry:
        #         speed = telemetry.speed
        #         print(round(speed * 2.23694, 2))

        # * demo - printing your current speed in assetto corsa
        # data = snapshot.get("lastestData")
        # if data:
        #     telemetry = data.get("RTCarData")
        #     if telemetry:
        #         speed = telemetry.speed_Mph
        #         print(speed)
        #     lapData = data.get("RTLapData")
        #     if lapData:
        #         lap = lapData.lap
        #         print(lap)

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def main() -> None:
    # Setup active metadata and local IP
    # ACTIVE_META = F12024MetaData
    # ACTIVE_META = BNGMetaData
    # ACTIVE_META = PC2MetaData
    # ACTIVE_META = FM7MetaData
    # ACTIVE_META = FM8MetaData
    ACTIVE_META = FH4MetaData
    # ACTIVE_META = FH5MetaData
    # ACTIVE_META = GT7MetaData
    # ACTIVE_META = ACMetaData

    # --

    localIP = "127.0.0.1"
    # localIP = "0.0.0.0"
    # localIP = ""

    # the ip of the device that is sending the data/ running the game
    # sendIP = "192.168.1.161"

    # setup
    activeThreads = telemetryManager()
    activeThreads.updateMeta(ACTIVE_META)
    activeThreads.updateLocalIP(localIP)
    # activeThreads.updateSendIP(localIP)

    activeThreads.addWorkerThread(example_worker_thread)

    activeThreads.StartTelemetry()

    # for packet, packetID, headerPacket in activeThreads.get_telemetry():
    #     if packetID == 6:
    #         if not packet:
    #             continue

    #         currnetPlayer = packet.m_carTelemetryData[0]
    #         speedValue = currnetPlayer.m_speed

    #         print(f"{speedValue} KPH")


if __name__ == "__main__":
    main()
