import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data_structures.GT7_struct import MetaData
from support.server import telemetryManager

# the IP of the PS5
sourceIP = "192.168.1.1"

telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)
telemetry.updateSendIP(sourceIP)

for packet, packetID, headerPacket in telemetry.get_telemetry():
    if not packet:
        continue

    packetName = packet.__name__

    # only if heartbeat msg is 'C'
    if packetName == "PacketCData":
        packetSpeed = packet.speed
        speedValue = round(packetSpeed * 3.6, 2)

        print(f"{speedValue} KPH")
