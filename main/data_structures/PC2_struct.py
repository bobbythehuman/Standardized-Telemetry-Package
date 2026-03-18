import ctypes
from enum import Enum

'''
packet information from
https://github.com/MacManley/project-cars-2-udp
and
https://web.archive.org/web/20220818194601/https://www.projectcarsgame.com/two/wp-content/uploads/sites/4/2018/01/sms_udp_definitions.hh
however this is outdated and the only one accessable from:
https://web.archive.org/web/20230201014848/https://www.projectcarsgame.com/two/project-cars-2-api/#1526544680534-1e10fcf7-b72a

'''

class DataTypes(Enum):
    STRUCTURE = ctypes.LittleEndianStructure
    # UNION = ctypes.Union

    SIGNED_BYTE = ctypes.c_byte
    SIGNED_SHORT = ctypes.c_short

    UNSIGNED_INT = ctypes.c_uint
    UNSIGNED_BYTE = ctypes.c_ubyte
    UNSIGNED_SHORT = ctypes.c_ushort

    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char


### Packet Header
#
#   Description: 
#    Base definitions of udp packet structure
#    The data definition mostly follows the data set for the Shared memory, so it is strongly suggested to have a look to the
#    latest shared memory header if you have problem decoding any data.
#

class PacketHeader(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs
    _fields_ = [
        ("mPacketNumber",           DataTypes.UNSIGNED_INT.value),     # Counter reflecting all the packets that have been sent during the game run
        ("mCategoryPacketNumber",   DataTypes.UNSIGNED_INT.value),     # Counter of the packet groups belonging to the given category
        ("mPartialPacketIndex",     DataTypes.UNSIGNED_BYTE.value),    # If the data from this class had to be sent in several packets, the index number
        ("mPartialPacketNumber",    DataTypes.UNSIGNED_BYTE.value),    # If the data from this class had to be sent in several packets, the total number
        ("mPacketType",             DataTypes.UNSIGNED_BYTE.value),    # What is the type of this packet (see EUDPStreamerPacketHanlderType for details)
        ("mPacketVersion",          DataTypes.UNSIGNED_BYTE.value),    # What is the version of protocol for this handler, to be bumped with data structure change
    ]


### Telemetry Packet -- Packet 0

#
#   Telemetry data for the viewed participant. 
#   Frequency: Each tick of the UDP streamer how it is set in the options
#   When it is sent: in race
#

class TelemetryData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (556 instead of at least 564 bytes)
    _fields_ = [
        ("s_header",                    PacketHeader),

        ("sViewedParticipantIndex",     DataTypes.SIGNED_BYTE.value),

        ("sUnfilteredThrottle",         DataTypes.UNSIGNED_BYTE.value),
        ("sUnfilteredBrake",            DataTypes.UNSIGNED_BYTE.value),
        ("sUnfilteredSteering",         DataTypes.SIGNED_BYTE.value),
        ("sUnfilteredClutch",           DataTypes.UNSIGNED_BYTE.value),

        ("sCarFlags",                   DataTypes.UNSIGNED_BYTE.value),
        ("sOilTempCelsius",             DataTypes.SIGNED_SHORT.value),
        ("sOilPressureKPa",             DataTypes.UNSIGNED_SHORT.value),
        ("sWaterTempCelsius",           DataTypes.SIGNED_SHORT.value),
        ("sWaterPressureKpa",           DataTypes.UNSIGNED_SHORT.value),
        ("sFuelPressureKpa",            DataTypes.UNSIGNED_SHORT.value),
        ("sFuelCapacity",               DataTypes.UNSIGNED_BYTE.value),
        ("sBrake",                      DataTypes.UNSIGNED_BYTE.value),
        ("sThrottle",                   DataTypes.UNSIGNED_BYTE.value),
        ("sClutch",                     DataTypes.UNSIGNED_BYTE.value),
        ("sFuelLevel",                  DataTypes.FLOAT.value),
        ("sSpeed",                      DataTypes.FLOAT.value),
        ("sRpm",                        DataTypes.UNSIGNED_SHORT.value),
        ("sMaxRpm",                     DataTypes.UNSIGNED_SHORT.value),
        ("sSteering",                   DataTypes.SIGNED_BYTE.value),
        ("sGearNumGears",               DataTypes.UNSIGNED_BYTE.value),
        ("sBoostAmount",                DataTypes.UNSIGNED_BYTE.value),
        ("sCrashState",                 DataTypes.UNSIGNED_BYTE.value),
        ("sOdometerKM",                 DataTypes.FLOAT.value),

        ("sOrientation",                DataTypes.FLOAT.value * 3),
        ("sLocalVelocity",              DataTypes.FLOAT.value * 3),
        ("sWorldVelocity",              DataTypes.FLOAT.value * 3),
        ("sAngularVelocity",            DataTypes.FLOAT.value * 3),
        ("sLocalAcceleration",          DataTypes.FLOAT.value * 3),
        ("sWorldAcceleration",          DataTypes.FLOAT.value * 3),
        ("sExtentsCentre",              DataTypes.FLOAT.value * 3),

        ("sTyreFlags",                  DataTypes.UNSIGNED_BYTE.value * 4),
        ("sTerrain",                    DataTypes.UNSIGNED_BYTE.value * 4),
        ("sTyreY",                      DataTypes.FLOAT.value * 4),
        ("sTyreRPS",                    DataTypes.FLOAT.value * 4),
        ("sTyreTemp",                   DataTypes.UNSIGNED_BYTE.value * 4),
        ("sTyreHeightAboveGround",      DataTypes.FLOAT.value * 4),
        ("sTyreWear",                   DataTypes.UNSIGNED_BYTE.value * 4),
        ("sBrakeDamage",                DataTypes.UNSIGNED_BYTE.value * 4),
        ("sSuspensionDamage",           DataTypes.UNSIGNED_BYTE.value * 4),
        ("sBrakeTempCelsius",           DataTypes.SIGNED_SHORT.value * 4),
        ("sTyreTreadTemp",              DataTypes.UNSIGNED_SHORT.value * 4),
        ("sTyreLayerTemp",              DataTypes.UNSIGNED_SHORT.value * 4),
        ("sTyreCarcassTemp",            DataTypes.UNSIGNED_SHORT.value * 4),
        ("sTyreRimTemp",                DataTypes.UNSIGNED_SHORT.value * 4),
        ("sTyreInternalAirTemp",        DataTypes.UNSIGNED_SHORT.value * 4),
        ("sTyreTempLeft",               DataTypes.UNSIGNED_SHORT.value * 4),
        ("sTyreTempCenter",             DataTypes.UNSIGNED_SHORT.value * 4),
        ("sTyreTempRight",              DataTypes.UNSIGNED_SHORT.value * 4),
        ("sWheelLocalPositionY",        DataTypes.FLOAT.value * 4),
        ("sRideHeight",                 DataTypes.FLOAT.value * 4),
        ("sSuspensionTravel",           DataTypes.FLOAT.value * 4),
        ("sSuspensionVelocity",         DataTypes.FLOAT.value * 4),
        ("sSuspensionRideHeight",       DataTypes.UNSIGNED_SHORT.value * 4),
        ("sAirPressure",                DataTypes.UNSIGNED_SHORT.value * 4),

        ("sEngineSpeed",                DataTypes.FLOAT.value),
        ("sEngineTorque",               DataTypes.FLOAT.value),
        ("sWings",                      DataTypes.UNSIGNED_BYTE.value * 2),
        ("sHandBrake",                  DataTypes.UNSIGNED_BYTE.value),

        ("sAeroDamage",                 DataTypes.UNSIGNED_BYTE.value),
        ("sEngineDamage",               DataTypes.UNSIGNED_BYTE.value),

        ("sJoyPad0",                    DataTypes.UNSIGNED_INT.value),
        ("sDPad",                       DataTypes.UNSIGNED_BYTE.value),
        ("sTyreCompound",               DataTypes.CHAR.value * 40 * 4),
        ("sTurboBoostPressure",         DataTypes.FLOAT.value),
        ("sFullPosition",               DataTypes.FLOAT.value * 3),
        ("sBrakeBias",                  DataTypes.UNSIGNED_BYTE.value),
        ("sTickCount",                  DataTypes.UNSIGNED_INT.value),
    ]


### Race Packet -- Packet 1

#
#   Race stats data.
#   Frequency: Logaritmic decrease
#   When it is sent: Counter resets on entering InRace state and again each time any of the values changes
#

class RaceData(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("s_header",                        PacketHeader),
        ("sWorldFastestLapTime",            DataTypes.FLOAT.value),
        ("sPersonalFastestLapTime",         DataTypes.FLOAT.value),
        ("sPersonalFastestSector1Time",     DataTypes.FLOAT.value),
        ("sPersonalFastestSector2Time",     DataTypes.FLOAT.value),
        ("sPersonalFastestSector3Time",     DataTypes.FLOAT.value),
        ("sWorldFastestSector1Time",        DataTypes.FLOAT.value),
        ("sWorldFastestSector2Time",        DataTypes.FLOAT.value),
        ("sWorldFastestSector3Time",        DataTypes.FLOAT.value),
        ("sTrackLength",                    DataTypes.FLOAT.value),
        ("sTrackLocation",                  DataTypes.CHAR.value * 64),
        ("sTrackVariation",                 DataTypes.CHAR.value * 64),
        ("sTranslatedTrackLocation",        DataTypes.CHAR.value * 64),
        ("sTranslatedTrackVariation",       DataTypes.CHAR.value * 64),
        ("sLapsTimeInEvent",                DataTypes.UNSIGNED_SHORT.value),
        ("sEnforcedPitStopLap",             DataTypes.SIGNED_BYTE.value),
    ]


### Participants Packet -- Packet 2

#
#   Participant names data.
#   Frequency: Logarithmic decrease
#   When it is sent: Counter resets on entering InRace state and again each  the participants change. 
#   The sParticipantsChangedTimestamp represent last time the participants has changed and is to be used to sync
#   this information with the rest of the participant related packets
#

class ParticipantsData(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("s_header",                        PacketHeader),
        ("sParticipantsChangedTimestamp",   DataTypes.UNSIGNED_INT.value),
        ("sName",                           DataTypes.CHAR.value * 64 * 16),
        ("sNationality",                    DataTypes.UNSIGNED_INT.value * 16),
        ("sIndex",                          DataTypes.UNSIGNED_SHORT.value * 16),
    ]


### Timings Packet -- Packet 3

#
#   Participant timings data. 
#   Frequency: Each tick of the UDP streamer how it is set in the options.
#   When it is sent: in race
#

class ParticipantsInfo(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1059 instead of at least 1192 bytes)
    _fields_ = [
        ("sWorldPosition",          DataTypes.SIGNED_SHORT.value * 3),
        ("sOrientation",            DataTypes.SIGNED_SHORT.value * 3),
        ("sCurrentLapDistance",     DataTypes.UNSIGNED_SHORT.value),
        ("sRacePosition",           DataTypes.UNSIGNED_BYTE.value),
        ("sSector",                 DataTypes.UNSIGNED_BYTE.value),
        ("sHighestFlag",            DataTypes.UNSIGNED_BYTE.value),
        ("sPitModeSchedule",        DataTypes.UNSIGNED_BYTE.value),
        ("sCarIndex",               DataTypes.UNSIGNED_SHORT.value),
        ("sRaceState",              DataTypes.UNSIGNED_BYTE.value),
        ("sCurrentLap",             DataTypes.UNSIGNED_BYTE.value),
        ("sCurrentTime",            DataTypes.FLOAT.value),
        ("sCurrentSectorTime",      DataTypes.FLOAT.value),
        ("sMPParticipantIndex",     DataTypes.UNSIGNED_SHORT.value),
    ]


class TimingsData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1059 instead of at least 1192 bytes)
    _fields_ = [
        ("s_header",                        PacketHeader),
        ("sNumParticipants",                DataTypes.SIGNED_BYTE.value),
        ("sParticipantsChangedTimestamp",   DataTypes.UNSIGNED_INT.value),
        ("sEventTimeRemaining",             DataTypes.FLOAT.value),
        ("sSplitTimeAhead",                 DataTypes.FLOAT.value),
        ("sSplitTimeBehind",                DataTypes.FLOAT.value),
        ("sSplitTime",                      DataTypes.FLOAT.value),
        ("sParticipants",                   ParticipantsInfo * 32),
        ("sLocalParticipantIndex",          DataTypes.UNSIGNED_SHORT.value),
        ("sTickCount",                      DataTypes.UNSIGNED_INT.value),
    ]


### Game State Packet -- Packet 4

#
#   Game State. 
#   Frequency: Each 5s while being in Main Menu, Each 10s while being in race + on each change Main Menu<->Race several times.
#   the frequency in Race is increased in case of weather timer being faster  up to each 5s for 30x time progression
#   When it is sent: Always
#

class GameStateData(DataTypes.STRUCTURE.value):
    _pack_ = 1
    _fields_ = [
        ("s_header",                PacketHeader),
        ("mBuildVersionNumber",     DataTypes.UNSIGNED_SHORT.value),
        ("mGameState",              DataTypes.CHAR.value),
        ("sAmbientTemperature",     DataTypes.SIGNED_BYTE.value),
        ("sTrackTemperature",       DataTypes.SIGNED_BYTE.value),
        ("sRainDensity",            DataTypes.UNSIGNED_BYTE.value),
        ("sSnowDensity",            DataTypes.UNSIGNED_BYTE.value),
        ("sWindSpeed",              DataTypes.SIGNED_BYTE.value),
        ("sWindDirectionX",         DataTypes.SIGNED_BYTE.value),
        ("sWindDirectionY",         DataTypes.SIGNED_BYTE.value),
    ]


### Time Stats Packet -- Packet 7

#
#   Participant Stats and records
#   Frequency: When entering the race and each time any of the values change, so basically each time any of the participants crosses a sector boundary.
#   When it is sent: In Race
#

class ParticipantStatsInfo(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("sFastestLapTime",         DataTypes.FLOAT.value),
        ("sLastLapTime",            DataTypes.FLOAT.value),
        ("sLastSectorTime",         DataTypes.FLOAT.value),
        ("sFastestSector1Time",     DataTypes.FLOAT.value),
        ("sFastestSector2Time",     DataTypes.FLOAT.value),
        ("sFastestSector3Time",     DataTypes.FLOAT.value),
        ("sParticipantOnlineRep",   DataTypes.UNSIGNED_INT.value),
        ("sMPParticipantIndex",     DataTypes.UNSIGNED_SHORT.value),
    ]


class ParticipantsStats(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("sParticipants",   ParticipantStatsInfo * 32),
    ]


class TimeStatsData(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("s_header",                        PacketHeader),
        ("sParticipantsChangedTimestamp",   DataTypes.UNSIGNED_INT.value),
        ("sStats",                          ParticipantsStats),
    ]


### Participants Vehicle Names Packet / Vehicle Class Names Packet -- Packet 8

#
#   Participant Vehicle names
#   Frequency: Logarithmic decrease
#   When it is sent: Counter resets on entering InRace state and again each  the participants change. 
#	The sParticipantsChangedTimestamp represent last time the participants has changed and is  to be used to sync 
#	this information with the rest of the participant related packets
#   Note: This data is always sent with at least 2 packets. The 1-(n-1) holds the vehicle name for each participant
#	The last one holding the class names.

class VehicleInfo(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("sIndex",  DataTypes.UNSIGNED_SHORT.value),
        ("sClass",  DataTypes.UNSIGNED_INT.value),
        ("sName",   DataTypes.CHAR.value * 64),
    ]


class ParticipantVehicleNamesData(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("s_header",        PacketHeader),
        ("sVehicleInfo",    VehicleInfo * 16),
    ]


class ClassInfo(DataTypes.STRUCTURE.value):
    _pack_ = 1
    _fields_ = [
        ("sClassIndex", DataTypes.UNSIGNED_INT.value),
        ("sName",       DataTypes.CHAR.value * 20),
    ]


class VehicleClassNamesData(DataTypes.STRUCTURE.value):
    _pack_ = 1
    _fields_ = [
        ("s_header",    PacketHeader),
        ("sClassInfo",  ClassInfo * 60),
    ]

### MetaData

class MetaData:
    port: int = 5606
    fullBufferSize: int = 1452
    headerInfo: tuple[int, type] = (12, PacketHeader)
    packetIDAttribute: str = 'mPacketType'
    packetInfo: dict[int, tuple[tuple[int, type], ...]] = {
        0: ((559, TelemetryData),),
        1: ((308, RaceData),),
        2: ((1136, ParticipantsData),),
        3: ((1063, TimingsData),),
        4: ((24, GameStateData),),
        7: ((1040, TimeStatsData),),
        8: ((1452, VehicleClassNamesData), (1164, ParticipantVehicleNamesData),),
    }




