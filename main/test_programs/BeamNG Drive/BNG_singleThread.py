import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data_structures.BNG_struct import MetaData
from support.server import telemetryManager

telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)

for packet, packetID, headerPacket in telemetry.get_telemetry():
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
