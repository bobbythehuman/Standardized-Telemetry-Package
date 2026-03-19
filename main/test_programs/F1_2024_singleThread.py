import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_structures.f1_2024_struct import MetaData
from support.server import get_telemetry

for packet, packetID, headerPacket in get_telemetry(MetaData):
    if not packet:
        continue

    packetName = packet.__name__

    if packetID == 6:
        currnetPlayer = packet.m_carTelemetryData[0]
        speedValue = currnetPlayer.m_speed

        print(f"{speedValue} KPH")
