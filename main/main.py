"""
Architecture:
    - Main thread   : creates storage, starts threads, waits for stop signal
    - Thread 1      : network listener — receives UDP data, decodes, writes to storage
    - Thread 2+     : user-defined worker threads with read-only access to storage
"""

from datetime import datetime
import threading

from support.server import ReadOnlyStorage, threadManager

from data_structures.projectCars2_packets import MetaData as PC2MetaData
from data_structures.f1_2024_struct import MetaData as F12024MetaData


def example_worker_thread(worker_id: int, ro_storage: ReadOnlyStorage, stop_event: threading.Event) -> None:
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()
        # -----------------------------------------------
        # do something here
        # -----------------------------------------------

        # demo - stopping within thread
        # a = input("enter [a]: ")
        # if a == "a":
        #     stop_event.set()

        # demo - printing your current speed in f1 24
        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("PacketCarTelemetryData")
            if telemetry:
                speed = telemetry.m_carTelemetryData[0].m_speed
                print(speed)

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def main() -> None:
    # Setup active metadata and local IP
    ACTIVE_META = F12024MetaData
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
