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

from datetime import datetime
import time
import threading

from support.server import ReadOnlyStorage, threadManager

from data_structures.projectCars2_packets import MetaData as PC2MetaData
from data_structures.f1_2024_struct import MetaData as F12024MetaData
from data_structures.beamng_drive import MetaData as BNGMetaData
from data_structures.FM8_struct import MetaData as FM8MetaData
from data_structures.FH5_struct import MetaData as FH5MetaData


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
        data = snapshot.get("lastestData")
        if data:
            # telemetry = data.get("SledData")
            # if telemetry:
            #     engRPM = telemetry.CurrentEngineRpm
            #     print(engRPM)
            telemetry = data.get("DashData")
            if telemetry:
                speed = telemetry.Speed
                print(round(speed * 2.23694, 2))

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def main() -> None:
    # Setup active metadata and local IP
    # ACTIVE_META = F12024MetaData
    # ACTIVE_META = BNGMetaData
    # ACTIVE_META = PC2MetaData
    # ACTIVE_META = FM8MetaData
    ACTIVE_META = FH5MetaData

    # localIP = "127.0.0.1"
    localIP = "0.0.0.0"

    activeThreads = threadManager()
    activeThreads.updateMeta(ACTIVE_META)
    activeThreads.updateIP(localIP)

    print("[MAIN] [INFO]\tStart at ", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

    # --------------------------------------------------------------
    # Worker Threads Here
    # --------------------------------------------------------------

    # you currently cant pass any arguments to your functions
    activeThreads.addWorkerThread(example_worker_thread)

    # activeThreads.addWorkerThread(worker_thread)

    # --------------------------------------------------------------

    # Starting all threads
    activeThreads.startThreads()

    # Wait for stop signal
    print("\n[MAIN] [INFO]\tRunning — press Ctrl+C to stop.")
    endProgram = ""
    try:
        while not activeThreads.isStillActive():
            activeThreads.wait(0.5)

            # only stop threads here if they dont get stopped any where else
            # endProgram = input(f"[q] to quit the program: ")
            # if endProgram.lower() == "q":
            #     activeThreads.triggerStop()

    except KeyboardInterrupt:
        print("\n[MAIN] [INFO]\tKeyboardInterrupt received.")
    finally:
        print("[MAIN] [INFO]\tStopping all threads\n")
        activeThreads.stopThreads()

    print("[MAIN] [INFO]\tEnd at ", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))


if __name__ == "__main__":
    main()
