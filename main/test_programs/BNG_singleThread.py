import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_structures.BNG_struct import MetaData
from support.server import get_telemetry

for packet, packetID, headerPacket in get_telemetry(MetaData):
    if not packet:
        continue

    packetName = packet.__name__

    # for the TelemetryData packet
    if packetName == "TelemetryData":
        packetSpeed = packet.speed
        speedValue = round(packetSpeed * 3.6, 2)

        print(f"{speedValue} KPH")

    # for the MotionSim packet
    if packetName == "MotionSim":
        format = packet.format

        print(f"Format: {format}")
