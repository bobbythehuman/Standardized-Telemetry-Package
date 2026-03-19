import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_structures.FM8_struct import MetaData
from support.server import get_telemetry

for packet, packetID, headerPacket in get_telemetry(MetaData):
    if not packet:
        continue

    packetName = packet.__name__

    # for the SledData packet
    if packetName == "SledData":
        engineRPM = packet.CurrentEngineRpm

        print(f"{engineRPM} RPM")

    # for the DashData packet
    if packetName == "DashData":
        packetSpeed = packet.Speed
        speedValue = round(packetSpeed * 3.6, 2)

        print(f"{speedValue} KPH")
