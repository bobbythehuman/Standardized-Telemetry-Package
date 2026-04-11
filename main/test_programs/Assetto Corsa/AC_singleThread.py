import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data_structures.AC_struct import MetaData
from support.server import telemetryManager

sourceIP = "127.0.0.1"

telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)
telemetry.updateSendIP(sourceIP)

for packet, packetID, headerPacket in telemetry.get_telemetry():
    if not packet:
        continue

    packetName = packet.__name__

    # for the TelemetryData packet
    if packetName == "RTCarData":
        packetSpeed = packet.speed_Mph
        speedValue = round(packetSpeed, 2)

        print(f"{speedValue} MPH")

    # for the MotionSim packet
    if packetName == "RTLapData":
        lap = packet.lap

        print(f"Lap: {lap}")
