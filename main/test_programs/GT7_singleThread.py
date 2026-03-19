import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_structures.GT7_struct import MetaData
from support.server import get_telemetry

# the UP of the PS5
sourceIP = "192.168.1.1"

for packet, packetID, headerPacket in get_telemetry(MetaData, destinationIP=sourceIP):
    if not packet:
        continue

    packetName = packet.__name__

    # only if heartbeat msg is 'C'
    if packetName == "PacketCData":
        packetSpeed = packet.speed
        speedValue = round(packetSpeed * 3.6, 2)

        print(f"{speedValue} KPH")
