import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data_structures.F1_2019_struct import MetaData
from support.server import telemetryManager

telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)

for packet, packetID, headerPacket in telemetry.get_telemetry():
    if not packet:
        continue

    packetName = packet.__name__

    if packetID == 6:
        currnetPlayer = packet.m_carTelemetryData[0]
        speedValue = currnetPlayer.m_speed

        print(f"{speedValue} KPH")
