import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_structures.PC2_struct import MetaData
from support.server import get_telemetry

for packet, packetID, headerPacket in get_telemetry(MetaData):
    if not packet:
        continue

    packetName = packet.__name__

    if packetID == 0:
        speedPacket = packet.sSpeed
        speedValue = round(speedPacket * 3.6, 2)

        print(f"{speedValue} KPH")

    if packetID == 8:
        if packetName == "ParticipantVehicleNamesData":
            currnetPlayer = packet.sVehicleInfo[0]
            currentCar = currnetPlayer.sName

            print(f"Car: {currentCar}")
