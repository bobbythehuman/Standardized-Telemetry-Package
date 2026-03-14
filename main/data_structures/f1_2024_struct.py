import ctypes
from enum import Enum


class DataTypes(Enum):
    STRUCTURE = ctypes.LittleEndianStructure
    UNION = ctypes.Union
    
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT16 = ctypes.c_int16
    # SIGNED_INT32 = ctypes.c_int32
    
    UNSIGNED_INT8 = ctypes.c_uint8
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT32 = ctypes.c_uint32
    UNSIGNED_INT64 = ctypes.c_uint64
    
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    DOUBLE = ctypes.c_double


### Packet Header


class PacketHeader(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (45 instead of at least 52 bytes)
    _fields_ = [
        ("m_packetFormat",              DataTypes.UNSIGNED_INT16.value),    # 2023
        ("m_gameYear",                  DataTypes.UNSIGNED_INT8.value),     # Game year - last two digits e.g. 23
        ("m_gameMajorVersion",          DataTypes.UNSIGNED_INT8.value),     # Game major version - "X.00"
        ("m_gameMinorVersion",          DataTypes.UNSIGNED_INT8.value),     # Game minor version - "1.XX"
        ("m_packetVersion",             DataTypes.UNSIGNED_INT8.value),     # Version of this packet type, all start from 1
        ("m_packetId",                  DataTypes.UNSIGNED_INT8.value),     # Identifier for the packet type, see below
        ("m_sessionUID",                DataTypes.UNSIGNED_INT64.value),    # Unique identifier for the session
        ("m_sessionTime",               DataTypes.FLOAT.value),             # Session timestamp
        ("m_frameIdentifier",           DataTypes.UNSIGNED_INT32.value),    # Identifier for the frame the data was retrieved on
        ("m_overallFrameIdentifier",    DataTypes.UNSIGNED_INT32.value),    # Overall identifier for the frame the data was retrieved on, doesn't go back after flashbacks
        ("m_playerCarIndex",            DataTypes.UNSIGNED_INT8.value),     # Index of player's car in the array
        ("m_secondaryPlayerCarIndex",   DataTypes.UNSIGNED_INT8.value),     # Index of secondary player's car in the array (splitscreen), 255 if no second player
    ]


### Motion Packet -- Rate as specified in menus -- 1349 bytes


class CarMotionData(DataTypes.STRUCTURE.value):
    # _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1349 instead of at least 1352 bytes)
    _fields_ = [
        ("m_worldPositionX",        DataTypes.FLOAT.value),         # World space X position
        ("m_worldPositionY",        DataTypes.FLOAT.value),         # World space Y position
        ("m_worldPositionZ",        DataTypes.FLOAT.value),         # World space Z position
        ("m_worldVelocityX",        DataTypes.FLOAT.value),         # Velocity in world space X
        ("m_worldVelocityY",        DataTypes.FLOAT.value),         # Velocity in world space Y
        ("m_worldVelocityZ",        DataTypes.FLOAT.value),         # Velocity in world space Z
        ("m_worldForwardDirX",      DataTypes.SIGNED_INT16.value),  # World space forward X direction (normalised)
        ("m_worldForwardDirY",      DataTypes.SIGNED_INT16.value),  # World space forward Y direction (normalised)
        ("m_worldForwardDirZ",      DataTypes.SIGNED_INT16.value),  # World space forward Z direction (normalised)
        ("m_worldRightDirX",        DataTypes.SIGNED_INT16.value),  # World space right X direction (normalised)
        ("m_worldRightDirY",        DataTypes.SIGNED_INT16.value),  # World space right Y direction (normalised)
        ("m_worldRightDirZ",        DataTypes.SIGNED_INT16.value),  # World space right Z direction (normalised)
        ("m_gForceLateral",         DataTypes.FLOAT.value),         # Lateral G-Force component
        ("m_gForceLongitudinal",    DataTypes.FLOAT.value),         # Longitudinal G-Force component
        ("m_gForceVertical",        DataTypes.FLOAT.value),         # Vertical G-Force component
        ("m_yaw",                   DataTypes.FLOAT.value),         # Yaw angle in radians
        ("m_pitch",                 DataTypes.FLOAT.value),         # Pitch angle in radians
        ("m_roll",                  DataTypes.FLOAT.value),         # Roll angle in radians
    ]


class PacketMotionData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1349 instead of at least 1352 bytes)
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carMotionData", CarMotionData * 22),    # Data for all cars on track
    ]


### Session Packet -- 2 per second -- 753 bytes


class MarshalZone(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (45 instead of at least 52 bytes)
    _fields_ = [
        ("m_zoneStart", DataTypes.FLOAT.value),         # Fraction (0..1) of way through the lap the marshal zone starts
        ("m_zoneFlag",  DataTypes.SIGNED_INT8.value),   # ZoneFlag in Appendices1
    ]


class WeatherForecastSample(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (753 instead of at least 828 bytes)
    _fields_ = [
        ("m_sessionType",               DataTypes.UNSIGNED_INT8.value), # SessionType in Appendices1
        ("m_timeOffset",                DataTypes.UNSIGNED_INT8.value), # Time in minutes the forecast is for
        ("m_weather",                   DataTypes.UNSIGNED_INT8.value), # Weather in Appendices1
        ("m_trackTemperature",          DataTypes.SIGNED_INT8.value),   # Track temp. in degrees Celsius
        ("m_trackTemperatureChange",    DataTypes.SIGNED_INT8.value),   # Track temp. TempChange in Appendices1
        ("m_airTemperature",            DataTypes.SIGNED_INT8.value),   # Air temp. in degrees celsius
        ("m_airTemperatureChange",      DataTypes.SIGNED_INT8.value),   # Air temp. TempChange in Appendices1
        ("m_rainPercentage",            DataTypes.UNSIGNED_INT8.value), # Rain percentage (0-100)
    ]


class PacketSessionData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (753 instead of at least 828 bytes)
    _fields_ = [
        ("m_header",                            PacketHeader),                          # Header
        ("m_weather",                           DataTypes.UNSIGNED_INT8.value),         # Weather in Appendices1
        ("m_trackTemperature",                  DataTypes.SIGNED_INT8.value),           # Track temp. in degrees celsius
        ("m_airTemperature",                    DataTypes.SIGNED_INT8.value),           # Air temp. in degrees celsius
        ("m_totalLaps",                         DataTypes.UNSIGNED_INT8.value),         # Total number of laps in this race
        ("m_trackLength",                       DataTypes.UNSIGNED_INT16.value),        # Track length in metres
        ("m_sessionType",                       DataTypes.UNSIGNED_INT8.value),         # SessionType in Appendices1
        ("m_trackId",                           DataTypes.SIGNED_INT8.value),           # Tracks in Appendices2
        ("m_formula",                           DataTypes.UNSIGNED_INT8.value),         # FormulaType in Appendices1
        ("m_sessionTimeLeft",                   DataTypes.UNSIGNED_INT16.value),        # Time left in session in seconds
        ("m_sessionDuration",                   DataTypes.UNSIGNED_INT16.value),        # Session duration in seconds
        ("m_pitSpeedLimit",                     DataTypes.UNSIGNED_INT8.value),         # Pit speed limit in kilometres per hour
        ("m_gamePaused",                        DataTypes.UNSIGNED_INT8.value),         # Whether the game is paused
        ("m_isSpectating",                      DataTypes.UNSIGNED_INT8.value),         # Whether the player is spectating
        ("m_spectatorCarIndex",                 DataTypes.UNSIGNED_INT8.value),         # Index of the car being spectated
        ("m_sliProNativeSupport",               DataTypes.UNSIGNED_INT8.value),         # SLI Pro support, Activeness in Appendices1
        ("m_numMarshalZones",                   DataTypes.UNSIGNED_INT8.value),         # Number of marshal zones to follow
        ("m_marshalZones",                      MarshalZone * 21),                      # List of marshal zones – max 21
        ("m_safetyCarStatus",                   DataTypes.UNSIGNED_INT8.value),         #SafetyCarStatus in Appendices1
        ("m_networkGame",                       DataTypes.UNSIGNED_INT8.value),         # NetworkStatus in Appendices1
        ("m_numWeatherForecastSamples",         DataTypes.UNSIGNED_INT8.value),         # Number of weather samples to follow
        ("m_weatherForecastSamples",            WeatherForecastSample * 64),            # Array of weather forecast samples
        ("m_forecastAccuracy",                  DataTypes.UNSIGNED_INT8.value),         # ForcastAccuracy in Appendices1
        ("m_aiDifficulty",                      DataTypes.UNSIGNED_INT8.value),         # AI Difficulty rating – 0-110
        ("m_seasonLinkIdentifier",              DataTypes.UNSIGNED_INT32.value),        # Identifier for season - persists across saves
        ("m_weekendLinkIdentifier",             DataTypes.UNSIGNED_INT32.value),        # Identifier for weekend - persists across saves
        ("m_sessionLinkIdentifier",             DataTypes.UNSIGNED_INT32.value),        # Identifier for session - persists across saves
        ("m_pitStopWindowIdealLap",             DataTypes.UNSIGNED_INT8.value),         # Ideal lap to pit on for current strategy (player)
        ("m_pitStopWindowLatestLap",            DataTypes.UNSIGNED_INT8.value),         # Latest lap to pit on for current strategy (player)
        ("m_pitStopRejoinPosition",             DataTypes.UNSIGNED_INT8.value),         # Predicted position to rejoin at (player)
        ("m_steeringAssist",                    DataTypes.UNSIGNED_INT8.value),         # AssistSwitch in Appendices1
        ("m_brakingAssist",                     DataTypes.UNSIGNED_INT8.value),         # BrakingAssist in Appendices1
        ("m_gearboxAssist",                     DataTypes.UNSIGNED_INT8.value),         # GearboxAssist in Appendices1
        ("m_pitAssist",                         DataTypes.UNSIGNED_INT8.value),         # AssistSwitch in Appendices1
        ("m_pitReleaseAssist",                  DataTypes.UNSIGNED_INT8.value),         # AssistSwitch in Appendices1
        ("m_ersAssist",                         DataTypes.UNSIGNED_INT8.value),         # AssistSwitch in Appendices1
        ("m_drsAssist",                         DataTypes.UNSIGNED_INT8.value),         # AssistSwitch in Appendices1
        ("m_dynamicRacingLine",                 DataTypes.UNSIGNED_INT8.value),         # RacinglineAssist in Appendices1
        ("m_dynamicRacingLineType",             DataTypes.UNSIGNED_INT8.value),         # RacinglineType in Appendices1
        ("m_gameMode",                          DataTypes.UNSIGNED_INT8.value),         # GameModes in Appendices2
        ("m_ruleSet",                           DataTypes.UNSIGNED_INT8.value),         # Rulesets in Appendices2
        ("m_timeOfDay",                         DataTypes.UNSIGNED_INT32.value),        # Local time of day - minutes since midnight
        ("m_sessionLength",                     DataTypes.UNSIGNED_INT8.value),         # SessionLength in Appendices1
        ("m_speedUnitsLeadPlayer",              DataTypes.UNSIGNED_INT8.value),         # SpeedUnits in Appendices1
        ("m_temperatureUnitsLeadPlayer",        DataTypes.UNSIGNED_INT8.value),         # TempUnits in Appendices1
        ("m_speedUnitsSecondaryPlayer",         DataTypes.UNSIGNED_INT8.value),         # SpeedUnits in Appendices1
        ("m_temperatureUnitsSecondaryPlayer",   DataTypes.UNSIGNED_INT8.value),         # TempUnits in Appendices1
        ("m_numSafetyCarPeriods",               DataTypes.UNSIGNED_INT8.value),         # Number of safety cars called during session
        ("m_numVirtualSafetyCarPeriods",        DataTypes.UNSIGNED_INT8.value),         # Number of virtual safety cars called
        ("m_numRedFlagPeriods",                 DataTypes.UNSIGNED_INT8.value),         # Number of red flags called during session
        ("m_equalCarPerformance",               DataTypes.UNSIGNED_INT8.value),         # 0 = Off, 1 = On
        ("m_recoveryMode",                      DataTypes.UNSIGNED_INT8.value),         # 0 = None, 1 = Flashbacks, 2 = Auto-recovery
        ("m_flashbackLimit",                    DataTypes.UNSIGNED_INT8.value),         # 0 = Low, 1 = Medium, 2 = High, 3 = Unlimited
        ("m_surfaceType",                       DataTypes.UNSIGNED_INT8.value),         # 0 = Simplified, 1 = Realistic
        ("m_lowFuelMode",                       DataTypes.UNSIGNED_INT8.value),         # 0 = Easy, 1 = Hard
        ("m_raceStarts",                        DataTypes.UNSIGNED_INT8.value),         # 0 = Manual, 1 = Assisted
        ("m_tyreTemperature",                   DataTypes.UNSIGNED_INT8.value),         # 0 = Surface only, 1 = Surface & Carcass
        ("m_pitLaneTyreSim",                    DataTypes.UNSIGNED_INT8.value),         # 0 = On, 1 = Off
        ("m_carDamage",                         DataTypes.UNSIGNED_INT8.value),         # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Simulation
        ("m_carDamageRate",                     DataTypes.UNSIGNED_INT8.value),         # 0 = Reduced, 1 = Standard, 2 = Simulation
        ("m_collisions",                        DataTypes.UNSIGNED_INT8.value),         # 0 = Off, 1 = Player-to-Player Off, 2 = On
        ("m_collisionsOffForFirstLapOnly",      DataTypes.UNSIGNED_INT8.value),         # 0 = Disabled, 1 = Enabled
        ("m_mpUnsafePitRelease",                DataTypes.UNSIGNED_INT8.value),         # 0 = On, 1 = Off (Multiplayer)
        ("m_mpOffForGriefing",                  DataTypes.UNSIGNED_INT8.value),         # 0 = Disabled, 1 = Enabled (Multiplayer)
        ("m_cornerCuttingStringency",           DataTypes.UNSIGNED_INT8.value),         # 0 = Regular, 1 = Strict
        ("m_parcFermeRules",                    DataTypes.UNSIGNED_INT8.value),         # 0 = Off, 1 = On
        ("m_pitStopExperience",                 DataTypes.UNSIGNED_INT8.value),         # 0 = Automatic, 1 = Broadcast, 2 = Immersive
        ("m_safetyCar",                         DataTypes.UNSIGNED_INT8.value),         # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Increased
        ("m_safetyCarExperience",               DataTypes.UNSIGNED_INT8.value),         # 0 = Broadcast, 1 = Immersive
        ("m_formationLap",                      DataTypes.UNSIGNED_INT8.value),         # 0 = Off, 1 = On
        ("m_formationLapExperience",            DataTypes.UNSIGNED_INT8.value),         # 0 = Broadcast, 1 = Immersive
        ("m_redFlags",                          DataTypes.UNSIGNED_INT8.value),         # 0 = Off, 1 = Reduced, 2 = Standard, 3 = Increased
        ("m_affectsLicenceLevelSolo",           DataTypes.UNSIGNED_INT8.value),         # 0 = Off, 1 = On
        ("m_affectsLicenceLevelMP",             DataTypes.UNSIGNED_INT8.value),         # 0 = Off, 1 = On
        ("m_numSessionsInWeekend",              DataTypes.UNSIGNED_INT8.value),         # Number of session in following array
        ("m_weekendStructure",                  DataTypes.UNSIGNED_INT8.value * 12),    # List of session types to show weekend structure
        ("m_sector2LapDistanceStart",           DataTypes.FLOAT.value),                 # Distance in m around track where sector 2 starts
        ("m_sector3LapDistanceStart",           DataTypes.FLOAT.value),                 # Distance in m around track where sector 3 starts
    ]


### Lap Data Packet -- Rate as specified in menus -- 1285 bytes


class LapData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (101 instead of at least 113 bytes)
    _fields_ = [
        ("m_lastLapTimeInMs",               DataTypes.UNSIGNED_INT32.value),    # Last lap time in milliseconds
        ("m_currentLapTimeInMs",            DataTypes.UNSIGNED_INT32.value),    # Current time around the lap in milliseconds
        ("m_sector1TimeInMs",               DataTypes.UNSIGNED_INT16.value),    # Sector 1 time in milliseconds
        ("m_sector1TimeInMinutes",          DataTypes.UNSIGNED_INT8.value),     # Sector 1 whole minute part
        ("m_sector2TimeInMs",               DataTypes.UNSIGNED_INT16.value),    # Sector 2 time in milliseconds
        ("m_sector2TimeInMinutes",          DataTypes.UNSIGNED_INT8.value),     # Sector 2 whole minute part
        ("m_deltaToCarInFrontMSPart",       DataTypes.UNSIGNED_INT16.value),    # Time delta to car in front milliseconds part
        ("m_deltaToCarInFrontMinutesPart",  DataTypes.UNSIGNED_INT8.value),     # Time delta to car in front whole minute part
        ("m_deltaToRaceLeaderMSPart",       DataTypes.UNSIGNED_INT16.value),    # Time delta to race leader milliseconds part
        ("m_deltaToRaceLeaderMinutesPart",  DataTypes.UNSIGNED_INT8.value),     # Time delta to race leader whole minute part
        ("m_lapDistance",                   DataTypes.FLOAT.value),             # Distance vehicle is around current lap in metres - can, be negative if line not crossed yet
        ("m_totalDistance",                 DataTypes.FLOAT.value),             # Total distance travelled in session in metres - can, be negative if line not crossed yet
        ("m_safetyCarDelta",                DataTypes.FLOAT.value),             # Delta in seconds for safety car
        ("m_car_position",                  DataTypes.UNSIGNED_INT8.value),     # Car race position
        ("m_currentLapNum",                 DataTypes.UNSIGNED_INT8.value),     # Current lap number
        ("m_pitStatus",                     DataTypes.UNSIGNED_INT8.value),     # PitStatus in Appendices1
        ("m_numPitStops",                   DataTypes.UNSIGNED_INT8.value),     # Number of pit stops taken in this race
        ("m_sector",                        DataTypes.UNSIGNED_INT8.value),     # Sector in Appendices1
        ("m_currentLapInvalid",             DataTypes.UNSIGNED_INT8.value),     # Current lap invalid - LapInvalidStatus in Appendices1
        ("m_penalties",                     DataTypes.UNSIGNED_INT8.value),     # Accumulated time penalties in seconds to be added
        ("m_totalWarnings",                 DataTypes.UNSIGNED_INT8.value),     # Accumulated number of warnings issued
        ("m_cornerCuttingWarnings",         DataTypes.UNSIGNED_INT8.value),     # Accumulated number of corners cutting warnings issued
        ("m_numUnservedDriveThroughPens",   DataTypes.UNSIGNED_INT8.value),     # Num drive through pens left to serve
        ("m_numUnservedStopGoPens",         DataTypes.UNSIGNED_INT8.value),     # Num stop go pens left to serve
        ("m_gridPosition",                  DataTypes.UNSIGNED_INT8.value),     # Grid position the vehicle started the race in
        ("m_driverStatus",                  DataTypes.UNSIGNED_INT8.value),     # Status of driver - DriverStatus in Appendices1
        ("m_resultStatus",                  DataTypes.UNSIGNED_INT8.value),     # Result status - ResultStatus in Appendices1
        ("m_pitLaneTimerActive",            DataTypes.UNSIGNED_INT8.value),     # Pit lane timing, Activeness in Appendices1
        ("m_pitLaneTimeInLaneInMs",         DataTypes.UNSIGNED_INT16.value),    # If active, the current time spent in the pit lane in ms
        ("m_pitStopTimerInMs",              DataTypes.UNSIGNED_INT16.value),    # Time of the actual pit stop in ms
        ("m_pitStopShouldServePen",         DataTypes.UNSIGNED_INT8.value),     # Whether the car should serve a penalty at this stop
        ("m_speedTrapFastestSpeed",         DataTypes.FLOAT.value),             # Time of the actual pit stop in ms
        ("m_speedTrapFastestLap",           DataTypes.UNSIGNED_INT8.value),     # Whether the car should serve a penalty at this stop
    ]


class PacketLapData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (101 instead of at least 113 bytes)
    _fields_ = [
        ("m_header",                PacketHeader),                      # Header
        ("m_lapData",               LapData * 22),                      # Lap data for all cars on track
        ("m_timeTrialPBCarIdx",     DataTypes.UNSIGNED_INT8.value),     # Index of Personal Best car in time trial (255 if invalid)
        ("m_timeTrialRivalCarIdx",  DataTypes.UNSIGNED_INT8.value),     # Index of Rival car in time trial (255 if invalid)
    ]


### Event Packet -- When the event occurs -- 45 bytes


class FastestLap(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8.value), # Vehicle index of car achieving fastest lap
        ("lapTime",     DataTypes.FLOAT.value),         # Lap time is in seconds
    ]


class Retirement(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8.value)  # Vehicle index of car retiring
    ]  


class TeamMateInPits(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8.value)  # Vehicle index of team mate
    ]  


class RaceWinner(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8.value)  # Vehicle index of the race winner
    ]  


class Penalty(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("penaltyType",         DataTypes.UNSIGNED_INT8.value), # PenaltyType in Appendices2
        ("infringementType",    DataTypes.UNSIGNED_INT8.value), # InfringmentType in Appendices2
        ("vehicleIdx",          DataTypes.UNSIGNED_INT8.value), # Vehicle index of the car the penalty is applied to
        ("otherVehicleIdx",     DataTypes.UNSIGNED_INT8.value), # Vehicle index of the other car involved
        ("time",                DataTypes.UNSIGNED_INT8.value), # Time gained, or time spent doing action in seconds
        ("lapNum",              DataTypes.UNSIGNED_INT8.value), # Lap the penalty occurred on
        ("placesGained",        DataTypes.UNSIGNED_INT8.value), # Number of places gained by this
    ]


class SpeedTrap(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (45 instead of at least 52 bytes)
    _fields_ = [
        ("vehicleIdx",                  DataTypes.UNSIGNED_INT8.value),     # Vehicle index of the vehicle triggering speed trap
        ("speed",                       DataTypes.FLOAT.value),             # Top speed achieved in kilometres per hour
        ("isOverallFastestInSession",   DataTypes.UNSIGNED_INT8.value),     # Overall fastest speed in InSession in Appendices1
        ("isDriverFastestInSession",    DataTypes.UNSIGNED_INT8.value),     # Fastest speed for driver InSession in Appendices1
        ("fastestVehicleIdxInSession",  DataTypes.UNSIGNED_INT8.value),     # Vehicle index of the vehicle that is the fastest in this session
        ("fastestSpeedInSession",       DataTypes.FLOAT.value),             # Speed of the vehicle that is the fastest in this session
    ]


class StartLIghts(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("numLights",   DataTypes.UNSIGNED_INT8.value)  # Number of lights showing
    ]


class DriveThroughPenaltyServed(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8.value)  # Vehicle index of the vehicle serving drive through
    ]


class StopGoPenaltyServed(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8.value)  # Vehicle index of the vehicle serving stop go
    ]


class Flashback(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("flashbackFrameIdentifier",    DataTypes.UNSIGNED_INT32.value),    # Frame identifier flashed back to
        ("flashbackSessionTime",        DataTypes.FLOAT.value),             # Session time flashed back to
    ]


class Buttons(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("m_buttonStatus",  DataTypes.UNSIGNED_INT32.value),    # Bit flags specifying which buttons are being pressed currently - ButtonFlags in Appendices2
    ]


class Overtake(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("overtakingVehicleIdx",        DataTypes.UNSIGNED_INT8.value), # Vehicle index of the vehicle overtaking
        ("beingOvertakenVehicleIdx",    DataTypes.UNSIGNED_INT8.value), # Vehicle index of the vehicle being overtaken
    ]


class SafetyCar(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("safetyCarType",   DataTypes.UNSIGNED_INT8.value), # 0 = No Safety Car, 1 = Full Safety Car, 2 = Virtual Safety Car, 3 = Formation Lap Safety Car
        ("eventType",       DataTypes.UNSIGNED_INT8.value), # 0 = Deployed, 1 = Returning, 2 = Returned, 3 = Resume Race
    ]


class Collision(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("vehicle1Idx", DataTypes.UNSIGNED_INT8.value), # Vehicle index of the first vehicle involved in the collision
        ("vehicle2Idx", DataTypes.UNSIGNED_INT8.value), # Vehicle index of the second vehicle involved in the collision
    ]


class EventDataDetails(DataTypes.UNION.value):
    _fields_ = [
        ("m_fastestLap",                FastestLap),
        ("m_retirement",                Retirement),
        ("m_teamMateInPits",            TeamMateInPits),
        ("m_raceWinner",                RaceWinner),
        ("m_penalty",                   Penalty),
        ("m_speedTrap",                 SpeedTrap),
        ("m_startLights",               StartLIghts),
        ("m_driveThroughPenaltyServed", DriveThroughPenaltyServed),
        ("m_stopGoPenaltyServed",       StopGoPenaltyServed),
        ("m_flashback",                 Flashback),
        ("m_buttons",                   Buttons),
        ("m_overtake",                  Overtake),
        ("m_safetyCar",                 SafetyCar),
        ("m_collision",                 Collision),
    ]


class PacketEventData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (45 instead of at least 52 bytes)
    _fields_ = [
        ("m_header",            PacketHeader),                      # Header
        ("m_eventStringCode",   DataTypes.UNSIGNED_INT8.value * 4), # Event string code, EventStringCode in Appendices2
        ("m_eventDetails",      EventDataDetails),                  # Event details - should be interpreted differently for each type
    ]


### Participants Packet -- Every 5 seconds -- 1350 bytes


class ParticipantData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1350 instead of at least 1394 bytes)
    _fields_ = [
        ("m_aiControlled",      DataTypes.UNSIGNED_INT8.value),     # Whether the vehicle is AiControlled in Appendices1
        ("m_driverId",          DataTypes.UNSIGNED_INT8.value),     # Driver id - Drivers in Appendices2
        ("m_networkId",         DataTypes.UNSIGNED_INT8.value),     # Network id – unique identifier for network players
        ("m_teamId",            DataTypes.UNSIGNED_INT8.value),     # Team id - Teams in Appendices2
        ("m_myTeam",            DataTypes.UNSIGNED_INT8.value),     # My team flag – MyTeamFlag in Appendices1
        ("m_raceNumber",        DataTypes.UNSIGNED_INT8.value),     # Race number of the car
        ("m_nationality",       DataTypes.UNSIGNED_INT8.value),     # Nationality of the driver
        ("m_name",              DataTypes.CHAR.value * 48),         # Name of participant in UTF-8 format – null terminated, Will be truncated with … (U+2026) if too long
        ("m_yourTelemetry",     DataTypes.UNSIGNED_INT8.value),     # The player's UDP setting, UdpStatus in Appendices1
        ("m_showOnlineNames",   DataTypes.UNSIGNED_INT8.value),     # The player's show online names setting, AssistSwitch in Appendices1
        ("m_techLevel",         DataTypes.UNSIGNED_INT16.value),    # F1 World tech level
        ("m_platform",          DataTypes.UNSIGNED_INT8.value),     # Platform in Appendices1
    ]


class PacketParticipantsData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1350 instead of at least 1394 bytes)
    _fields_ = [
        ("m_header",            PacketHeader),                      # Header
        ("m_numActiveCars",     DataTypes.UNSIGNED_INT8.value),     # Number of active cars in the data – should match number of cars on HUD
        ("m_participants",      ParticipantData * 22),
    ]


### Car Setups Packet -- 2 per second -- 1133 bytes


class CarSetupData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1133 instead of at least 1268 bytes)
    _fields_ = [
        ("m_frontWing",                 DataTypes.UNSIGNED_INT8.value),     # Front wing aero
        ("m_rearWing",                  DataTypes.UNSIGNED_INT8.value),     # Rear wing aero
        ("m_onThrottle",                DataTypes.UNSIGNED_INT8.value),     # Differential adjustment on throttle (percentage)
        ("m_offThrottle",               DataTypes.UNSIGNED_INT8.value),     # Differential adjustment off throttle (percentage)
        ("m_frontCamber",               DataTypes.FLOAT.value),             # Front camber angle (suspension geometry)
        ("m_rearCamber",                DataTypes.FLOAT.value),             # Rear camber angle (suspension geometry)
        ("m_frontToe",                  DataTypes.FLOAT.value),             # Front toe angle (suspension geometry)
        ("m_rearToe",                   DataTypes.FLOAT.value),             # Rear toe angle (suspension geometry)
        ("m_frontSuspension",           DataTypes.UNSIGNED_INT8.value),     # Front suspension
        ("m_rearSuspension",            DataTypes.UNSIGNED_INT8.value),     # Rear suspension
        ("m_frontAntiRollBar",          DataTypes.UNSIGNED_INT8.value),     # Front anti-roll bar
        ("m_rearAntiRollBar",           DataTypes.UNSIGNED_INT8.value),     # Front anti-roll bar
        ("m_frontSuspensionHeight",     DataTypes.UNSIGNED_INT8.value),     # Front ride height
        ("m_rearSuspensionHeight",      DataTypes.UNSIGNED_INT8.value),     # Rear ride height
        ("m_brakePressure",             DataTypes.UNSIGNED_INT8.value),     # Brake pressure (percentage)
        ("m_brakeBias",                 DataTypes.UNSIGNED_INT8.value),     # Brake bias (percentage)
        ("m_engineBraking",             DataTypes.UNSIGNED_INT8.value),     # Engine braking (percentage)
        ("m_rearLeftTyrePressure",      DataTypes.FLOAT.value),             # Rear left tyre pressure (PSI)
        ("m_rearRightTyrePressure",     DataTypes.FLOAT.value),             # Rear right tyre pressure (PSI)
        ("m_frontLeftTyrePressure",     DataTypes.FLOAT.value),             # Front left tyre pressure (PSI)
        ("m_frontRightTyrePressure",    DataTypes.FLOAT.value),             # Front right tyre pressure (PSI)
        ("m_ballast",                   DataTypes.UNSIGNED_INT8.value),     # Ballast
        ("m_fuelLoad",                  DataTypes.FLOAT.value),             # Fuel load
    ]


class PacketCarSetupData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1133 instead of at least 1268 bytes)
    _fields_ = [
        ("m_header",                PacketHeader),              # Header
        ("m_car_setups",            CarSetupData * 22),
        ("m_nextFrontWingValue",    DataTypes.FLOAT.value),     # Value of front wing after next pit stop - player only
    ]


### Car Telemetry Packet -- Rate as specified in menus -- 1352 bytes


class CarTelemetryData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1352 instead of at least 1444 bytes)
    _fields_ = [
        ("m_speed",                     DataTypes.UNSIGNED_INT16.value),        # Speed of car in kilometres per hour
        ("m_throttle",                  DataTypes.FLOAT.value),                 # Amount of throttle applied (0.0 to 1.0)
        ("m_steer",                     DataTypes.FLOAT.value),                 # Steering (-1.0 (full lock left) to 1.0 (full lock right))
        ("m_brake",                     DataTypes.FLOAT.value),                 # Amount of brake applied (0.0 to 1.0)
        ("m_clutch",                    DataTypes.UNSIGNED_INT8.value),         # Amount of clutch applied (0 to 100)
        ("m_gear",                      DataTypes.SIGNED_INT8.value),           # Gear selected (1-8, N=0, R=-1)
        ("m_engineRpm",                 DataTypes.UNSIGNED_INT16.value),        # Engine RPM
        ("m_drs",                       DataTypes.UNSIGNED_INT8.value),         # AssistSwitch in Appendices1
        ("m_revLightsPercent",          DataTypes.UNSIGNED_INT8.value),         # Rev lights indicator (percentage)
        ("m_revLightsBitValue",         DataTypes.UNSIGNED_INT16.value),        # Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
        ("m_brakesTemperature",         DataTypes.UNSIGNED_INT16.value * 4),    # Brakes temperature (celsius)
        ("m_tyresSurfaceTemperature",   DataTypes.UNSIGNED_INT8.value * 4),     # Tyres surface temperature (celsius)
        ("m_tyresInnerTemperature",     DataTypes.UNSIGNED_INT8.value * 4),     # Tyres inner temperature (celsius)
        ("m_engineTemperature",         DataTypes.UNSIGNED_INT16.value),        # Engine temperature (celsius)
        ("m_tyresPressure",             DataTypes.FLOAT.value * 4),             # Tyres pressure (PSI)
        ("m_surfaceType",               DataTypes.UNSIGNED_INT8.value * 4),     # Driving surface, SurfaceType in Appendices2
    ]


class PacketCarTelemetryData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1352 instead of at least 1444 bytes)
    _fields_ = [
        ("m_header",                        PacketHeader),                      # Header
        ("m_carTelemetryData",              CarTelemetryData * 22),
        ("m_mfdPanelIndex",                 DataTypes.UNSIGNED_INT8.value),     # Index of MFD panel open - MfdPanel  in Appendices1, May vary depending on game mode
        ("m_mfdPanelIndexSecondaryPlayer",  DataTypes.UNSIGNED_INT8.value),     # See above
        ("m_suggestedGear",                 DataTypes.SIGNED_INT8.value),       # Suggested gear for the player (1-8), 0 if no gear suggested
    ]


### Car Status Packet -- Rate as specified in menus -- 1239 bytes


class CarStatusData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1239 instead of at least 1440 bytes)
    _fields_ = [
        ("m_tractionControl",           DataTypes.UNSIGNED_INT8.value),     # Traction control - TractionStatus in Appendices1
        ("m_antiLockBrakes",            DataTypes.UNSIGNED_INT8.value),     # AssistSwitch in Appendices1
        ("m_fuelMix",                   DataTypes.UNSIGNED_INT8.value),     # Fuel mix - FuelMix in Appendices1
        ("m_frontBrakeBias",            DataTypes.UNSIGNED_INT8.value),     # Front brake bias (percentage)
        ("m_pitLimiterStatus",          DataTypes.UNSIGNED_INT8.value),     # Pit limiter status - AssistSwitch in Appendices1
        ("m_fuelInTank",                DataTypes.FLOAT.value),             # Current fuel mass
        ("m_fuelCapacity",              DataTypes.FLOAT.value),             # Fuel capacity
        ("m_fuelRemainingLaps",         DataTypes.FLOAT.value),             # Fuel remaining in terms of laps (value on MFD)
        ("m_maxRpm",                    DataTypes.UNSIGNED_INT16.value),    # Cars max RPM, point of rev limiter
        ("m_idleRpm",                   DataTypes.UNSIGNED_INT16.value),    # Cars idle RPM
        ("m_maxGears",                  DataTypes.UNSIGNED_INT8.value),     # Maximum number of gears
        ("m_drsAllowed",                DataTypes.UNSIGNED_INT8.value),     # DrsAllowed in Appendices1
        ("m_drsActivationDistance",     DataTypes.UNSIGNED_INT16.value),    # 0 = DRS not available, non-zero - DRS will be available in [X] metres
        ("m_actualTyreCompound",        DataTypes.UNSIGNED_INT8.value),     # ActualTyres in Appendices1
        ("m_visualTyreCompound",        DataTypes.UNSIGNED_INT8.value),     # VisualTyres in Appendices1
        ("m_tyresAgeLaps",              DataTypes.UNSIGNED_INT8.value),     # Age in laps of the current set of tyres
        ("m_vehicleFiaFlags",           DataTypes.SIGNED_INT8.value),       # VehicleFlag in Appendices1
        ("m_enginePowerICE",            DataTypes.FLOAT.value),             # Engine power output of ICE (W)
        ("m_enginePowerMGUK",           DataTypes.FLOAT.value),             # Engine power output of MGU-K (W)
        ("m_ersStoreEnergy",            DataTypes.FLOAT.value),             # ERS energy store in Joules
        ("m_ersDeployMode",             DataTypes.UNSIGNED_INT8.value),     # ERS deployment mode, DeployMode in Appendices1
        ("m_ersHarvestedThisLapMguk",   DataTypes.FLOAT.value),             # ERS energy harvested this lap by MGU-K
        ("m_ersHarvestedThisLapMguh",   DataTypes.FLOAT.value),             # ERS energy harvested this lap by MGU-H
        ("m_ersDeployedThisLap",        DataTypes.FLOAT.value),             # ERS energy deployed this lap
        ("m_networkPaused",             DataTypes.UNSIGNED_INT8.value),     # Whether the car is paused in a network game
    ]


class PacketCarStatusData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1239 instead of at least 1440 bytes)
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carStatusData", CarStatusData * 22),
    ]


### Final Classification Packet -- Once at the end of a race -- 1020 bytes


class FinalClassificationData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1020 instead of at least 1264 bytes)
    _fields_ = [
        ("m_position",          DataTypes.UNSIGNED_INT8.value),         # Finishing position
        ("m_numLaps",           DataTypes.UNSIGNED_INT8.value),         # Number of laps completed
        ("m_gridPosition",      DataTypes.UNSIGNED_INT8.value),         # Grid position of the car
        ("m_points",            DataTypes.UNSIGNED_INT8.value),         # Number of points scored
        ("m_numPitStops",       DataTypes.UNSIGNED_INT8.value),         # Number of pit stops made
        ("m_resultStatus",      DataTypes.UNSIGNED_INT8.value),         # Result status - ResultStatus in Appendices1
        ("m_bestLapTimeInMs",   DataTypes.UNSIGNED_INT32.value),        # Best lap time of the session in milliseconds
        ("m_totalRaceTime",     DataTypes.DOUBLE.value),                # Total race time in seconds without penalties
        ("m_penaltiesTime",     DataTypes.UNSIGNED_INT8.value),         # Total penalties accumulated in seconds
        ("m_numPenalties",      DataTypes.UNSIGNED_INT8.value),         # Number of penalties applied to this driver
        ("m_numTyreStints",     DataTypes.UNSIGNED_INT8.value),         # Number of tyres stints up to maximum
        ("m_tyreStintsActual",  DataTypes.UNSIGNED_INT8.value * 8),     # Actual tyres used by this driver
        ("m_tyreStintsVisual",  DataTypes.UNSIGNED_INT8.value * 8),     # Visual tyres used by this driver
        ("tyreStintsEndLaps",   DataTypes.UNSIGNED_INT8.value * 8),     # The lap number stints end on
    ]


class PacketFinalClassificationData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1020 instead of at least 1264 bytes)
    _fields_ = [
        ("m_header",                PacketHeader),                      # Header
        ("m_numCars",               DataTypes.UNSIGNED_INT8.value),     # Number of cars in the final classification
        ("m_classificationData",    FinalClassificationData * 22),
    ]


### Lobby Info Packet -- Two every second when in the lobby -- 1306 bytes


class LobbyInfoData(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("m_aiControlled",      DataTypes.UNSIGNED_INT8.value),     # Whether the vehicle is AI (1) or Human (0) controlled
        ("m_teamId",            DataTypes.UNSIGNED_INT8.value),     # Team id - see appendix (255 if no team currently selected)
        ("m_nationality",       DataTypes.UNSIGNED_INT8.value),     # Nationality of the driver
        ("m_platform",          DataTypes.UNSIGNED_INT8.value),     # Platform in Appendices1
        ("m_name",              DataTypes.CHAR.value * 48),         # Name of participant in UTF-8 format – null terminated Will be truncated with ... (U+2026) if too long
        ("m_carNumber",         DataTypes.UNSIGNED_INT8.value),     # Car number of the player
        ("m_yourTelemetry",     DataTypes.UNSIGNED_INT8.value),     # The player's UDP setting, 0 = restricted, 1 = public
        ("m_showOnlineNames",   DataTypes.UNSIGNED_INT8.value),     # The player's show online names setting, 0 = off, 1 = on
        ("m_techLevel",         DataTypes.UNSIGNED_INT16.value),    # F1 World tech level
        ("m_readyStatus",       DataTypes.UNSIGNED_INT8.value),     # ReadyStatus in Appendices1
    ]


class PacketLobbyInfoData(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("m_header",        PacketHeader),                      # Header Packet specific data
        ("m_numPlayers",    DataTypes.UNSIGNED_INT8.value),     # Number of players in the lobby data
        ("m_lobbyPlayers",  LobbyInfoData * 22),
    ]


### Car Damage Packet -- 10 per second -- 953 bytes


class CarDamageData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (953 instead of at least 1000 bytes)
    _fields_ = [
        ("m_tyresWear",             DataTypes.FLOAT.value * 4),             # Tyre wear (percentage)
        ("m_tyresDamage",           DataTypes.UNSIGNED_INT8.value * 4),     # Tyre damage (percentage)
        ("m_brakesDamage",          DataTypes.UNSIGNED_INT8.value * 4),     # Brakes damage (percentage)
        ("m_frontLeftWingDamage",   DataTypes.UNSIGNED_INT8.value),         # Front left wing damage (percentage)
        ("m_frontRightWingDamage",  DataTypes.UNSIGNED_INT8.value),         # Front right wing damage (percentage)
        ("m_rearWingDamage",        DataTypes.UNSIGNED_INT8.value),         # Rear wing damage (percentage)
        ("m_floorDamage",           DataTypes.UNSIGNED_INT8.value),         # Floor damage (percentage)
        ("m_diffuserDamage",        DataTypes.UNSIGNED_INT8.value),         # Diffuser damage (percentage)
        ("m_sidepodDamage",         DataTypes.UNSIGNED_INT8.value),         # Sidepod damage (percentage)
        ("m_drsFault",              DataTypes.UNSIGNED_INT8.value),         # Indicator for DRS fault, Fault in Appendices1
        ("m_ersFault",              DataTypes.UNSIGNED_INT8.value),         # Indicator for ERS fault, Fault in Appendices1
        ("m_gearBoxDamage",         DataTypes.UNSIGNED_INT8.value),         # Gear box damage (percentage)
        ("m_engineDamage",          DataTypes.UNSIGNED_INT8.value),         # Engine damage (percentage)
        ("m_engineMguhwear",        DataTypes.UNSIGNED_INT8.value),         # Engine wear MGU-H (percentage)
        ("m_engineEswear",          DataTypes.UNSIGNED_INT8.value),         # Engine wear ES (percentage)
        ("m_engineCewear",          DataTypes.UNSIGNED_INT8.value),         # Engine wear CE (percentage)
        ("m_engineIcewear",         DataTypes.UNSIGNED_INT8.value),         # Engine wear ICE (percentage)
        ("m_engineMgukwear",        DataTypes.UNSIGNED_INT8.value),         # Engine wear MGU-K (percentage)
        ("m_engineTcwear",          DataTypes.UNSIGNED_INT8.value),         # Engine wear TC (percentage)
        ("m_engineBlown",           DataTypes.UNSIGNED_INT8.value),         # Engine blown, Fault in Appendices1
        ("m_engineSeized",          DataTypes.UNSIGNED_INT8.value),         # Engine seized, Fault in Appendices1
    ]


class PacketCarDamageData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (953 instead of at least 1000 bytes)
    _fields_ = [
        ("m_header",            PacketHeader),          # Header
        ("m_carDamageData",     CarDamageData * 22),
    ]


### Session History Packet -- 20 per second but cycling through cars -- 1460 bytes


class LapHistoryData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1460 instead of at least 1660 bytes)
    _fields_ = [
        ("m_lapTimeInMs",           DataTypes.UNSIGNED_INT32.value),    # Lap time in milliseconds
        ("m_sector1TimeInMs",       DataTypes.UNSIGNED_INT16.value),    # Sector 1 time in milliseconds
        ("m_sector1TimeMinutes",    DataTypes.UNSIGNED_INT8.value),     # Sector 1 whole minute part
        ("m_sector2TimeInMs",       DataTypes.UNSIGNED_INT16.value),    # Sector 2 time in millisecond
        ("m_sector2TimeMinutes",    DataTypes.UNSIGNED_INT8.value),     # Sector 2 whole minute part
        ("m_sector3TimeInMs",       DataTypes.UNSIGNED_INT16.value),    # Sector 3 time in milliseconds
        ("m_sector3TimeMinutes",    DataTypes.UNSIGNED_INT8.value),     # Sector 3 whole minute part
        ("m_lapValidBitFlags",      DataTypes.UNSIGNED_INT8.value),     # ValidBitFlag in Appendices1
    ]


class TyreStintHistoryData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1460 instead of at least 1660 bytes)
    _fields_ = [
        ("m_endLap",                DataTypes.UNSIGNED_INT8.value),     # Lap the tyre usage ends on (255 of current tyre)
        ("m_tyreActualCompound",    DataTypes.UNSIGNED_INT8.value),     # Actual tyres used by this driver
        ("m_tyreVisualCompound",    DataTypes.UNSIGNED_INT8.value),     # Visual tyres used by this driver
    ]


class PacketSessionHistoryData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1460 instead of at least 1660 bytes)
    _fields_ = [
        ("m_header",                    PacketHeader),                      # Header
        ("m_carIdx",                    DataTypes.UNSIGNED_INT8.value),     # Index of the car this lap data relates to
        ("m_numLaps",                   DataTypes.UNSIGNED_INT8.value),     # Num laps in the data (including current partial lap)
        ("m_numTyreStints",             DataTypes.UNSIGNED_INT8.value),     # Number of tyre stints in the data
        ("m_bestLapTimeLapNum",         DataTypes.UNSIGNED_INT8.value),     # Lap the best lap time was achieved on
        ("m_bestSector1LapNum",         DataTypes.UNSIGNED_INT8.value),     # Lap the best Sector 1 time was achieved on
        ("m_bestSector2LapNum",         DataTypes.UNSIGNED_INT8.value),     # Lap the best Sector 2 time was achieved on
        ("m_bestSector3LapNum",         DataTypes.UNSIGNED_INT8.value),     # Lap the best Sector 3 time was achieved on
        ("m_lapHistoryData",            LapHistoryData * 100),              # 100 laps of data max
        ("m_tyreStintsHistoryData",     TyreStintHistoryData * 8),
    ]


### Tyre Set Packet -- 20 per second but cycling through cars -- 231 bytes


class TyreSetData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (231 instead of at least 272 bytes)
    _fields_ = [
        ("m_actualTyreCompound",    DataTypes.UNSIGNED_INT8.value),     # Actual tyre compound used
        ("m_visualTyreCompound",    DataTypes.UNSIGNED_INT8.value),     # Visual tyre compound used
        ("m_wear",                  DataTypes.UNSIGNED_INT8.value),     # Tyre wear (percentage)
        ("m_available",             DataTypes.UNSIGNED_INT8.value),     # Whether this set is currently available
        ("m_recommendedSession",    DataTypes.UNSIGNED_INT8.value),     # Recommended session for tyre set
        ("m_lifeSpan",              DataTypes.UNSIGNED_INT8.value),     # Laps left in this tyre set
        ("m_usableLife",            DataTypes.UNSIGNED_INT8.value),     # Max number of laps recommended for this compound
        ("m_lapDeltaTime",          DataTypes.SIGNED_INT16.value),      # Lap delta time in milliseconds compared to fitted set
        ("m_fitted",                DataTypes.UNSIGNED_INT8.value),     # Whether the set is fitted or not
    ]


class PacketTyreSetsData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (231 instead of at least 272 bytes)
    _fields_ = [
        ("m_header",        PacketHeader),                      # Header
        ("m_carIdx",        DataTypes.UNSIGNED_INT8.value),     # Index of the car this data relates to
        ("m_tyreSetData",   TyreSetData * 20),                  # 13 (dry) + 7 (wet)
        ("m_fittedIdx",     DataTypes.UNSIGNED_INT8.value),     # Index into array of fitted tyre
    ]


### Motion Ex Packet -- Rate as specified in menus -- 237 bytes


class PacketMotionExData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (237 instead of at least 240 bytes)
    _fields_ = [
        ("m_header",    PacketHeader),  # Header
        # Extra player car ONLY data
        ("m_suspensionPosition",        DataTypes.FLOAT.value * 4),     # Note: All wheel arrays have the following order:
        ("m_suspensionVelocity",        DataTypes.FLOAT.value * 4),     # RL, RR, FL, FR
        ("m_suspensionAcceleration",    DataTypes.FLOAT.value * 4),     # RL, RR, FL, FR
        ("m_wheelSpeed",                DataTypes.FLOAT.value * 4),     # Speed of each wheel
        ("m_wheelSlipRatio",            DataTypes.FLOAT.value * 4),     # Slip ratio for each wheel
        ("m_wheelSlipAngle",            DataTypes.FLOAT.value * 4),     # Slip angles for each wheel
        ("m_wheelLatForce",             DataTypes.FLOAT.value * 4),     # Lateral forces for each wheel
        ("m_wheelLongForce",            DataTypes.FLOAT.value * 4),     # Longitudinal forces for each wheel
        ("m_heightOfCOGAboveGround",    DataTypes.FLOAT.value),         # Height of centre of gravity above ground
        ("m_localVelocityX",            DataTypes.FLOAT.value),         # Velocity in local space – metres/s
        ("m_localVelocityY",            DataTypes.FLOAT.value),         # Velocity in local space
        ("m_localVelocityZ",            DataTypes.FLOAT.value),         # Velocity in local space
        ("m_angularVelocityX",          DataTypes.FLOAT.value),         # Angular velocity x-component – metres/s
        ("m_angularVelocityY",          DataTypes.FLOAT.value),         # Angular velocity y-component
        ("m_angularVelocityZ",          DataTypes.FLOAT.value),         # Angular velocity z-component
        ("m_angularAccelerationX",      DataTypes.FLOAT.value),         # Angular acceleration x-component – metres/s
        ("m_angularAccelerationY",      DataTypes.FLOAT.value),         # Angular acceleration y-component
        ("m_angularAccelerationZ",      DataTypes.FLOAT.value),         # Angular acceleration z-component
        ("m_frontWheelsAngle",          DataTypes.FLOAT.value),         # Current front wheels angle in radians
        ("m_wheelVertForce",            DataTypes.FLOAT.value * 4),     # Vertical forces for each wheel
        ("m_frontAeroHeight",           DataTypes.FLOAT.value),         # Front plank edge height above road surface
        ("m_rearAeroHeight",            DataTypes.FLOAT.value),         # Rear plank edge height above road surface
        ("m_frontRollAngle",            DataTypes.FLOAT.value),         # Roll angle of the front suspension
        ("m_rearRollAngle",             DataTypes.FLOAT.value),         # Roll angle of the rear suspension
        ("m_chassisYaw",                DataTypes.FLOAT.value),         # Yaw angle of the chassis relative to the direction of motion - radians
    ]


### Time Trial Packet -- 1 per second, only in time trial -- 101 bytes


class TimeTrialDataSet(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (101 instead of at least 116 bytes)
    _fields_ = [
        ("m_carIdx",                DataTypes.UNSIGNED_INT8.value),     # Index of the car this data relates to
        ("m_teamId",                DataTypes.UNSIGNED_INT8.value),     # Team id - see appendix
        ("m_lapTimeInMS",           DataTypes.UNSIGNED_INT32.value),    # Lap time in milliseconds
        ("m_sector1TimeInMS",       DataTypes.UNSIGNED_INT32.value),    # Sector 1 time in milliseconds
        ("m_sector2TimeInMS",       DataTypes.UNSIGNED_INT32.value),    # Sector 2 time in milliseconds
        ("m_sector3TimeInMS",       DataTypes.UNSIGNED_INT32.value),    # Sector 3 time in milliseconds
        ("m_tractionControl",       DataTypes.UNSIGNED_INT8.value),     # 0 = off, 1 = medium, 2 = full
        ("m_gearboxAssist",         DataTypes.UNSIGNED_INT8.value),     # 1 = manual, 2 = manual & suggested gear, 3 = auto
        ("m_antiLockBrakes",        DataTypes.UNSIGNED_INT8.value),     # 0 (off) - 1 (on)
        ("m_equalCarPerformance",   DataTypes.UNSIGNED_INT8.value),     # 0 = Realistic, 1 = Equal
        ("m_customSetup",           DataTypes.UNSIGNED_INT8.value),     # 0 = No, 1 = Yes
        ("m_valid",                 DataTypes.UNSIGNED_INT8.value),     # 0 = invalid, 1 = valid
    ]


class PacketTimeTrialData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (101 instead of at least 116 bytes)
    _fields_ = [
        ("m_header",                    PacketHeader),      # Header
        ("m_playerSessionBestDataSet",  TimeTrialDataSet),  # Player session best data set
        ("m_personalBestDataSet",       TimeTrialDataSet),  # Personal best data set
        ("m_rivalDataSet",              TimeTrialDataSet),  # Rival data set
    ]


### MetaData

class MetaData:
    port: int = 20777
    fullBufferSize: int = 1464
    headerInfo: tuple[int, type] = (32, PacketHeader)
    packetIDAttribute: str = "m_packetId"
    packetInfo: dict[int, tuple[tuple[int, type], ...]] = {
        0: ((1349, PacketMotionData),), # Motion
        1: ((753, PacketSessionData),), # Session
        2: ((1285, PacketLapData),), # Participants
        3: ((45, PacketEventData),), # Car Setups
        4: ((1350, PacketParticipantsData),), # Car Telemetry
        5: ((1133, PacketCarSetupData),), # Car Status
        6: ((1352, PacketCarTelemetryData),), # Final Classification
        7: ((1239, PacketCarStatusData),), # Lobby Info
        8: ((1020, PacketFinalClassificationData),), # Car Damage
        9: ((1306, PacketLobbyInfoData),), # Session History
        10: ((953, PacketCarDamageData),), # Tyre Sets
        11: ((1460, PacketSessionHistoryData),), # Motion Ex
        12: ((231, PacketTyreSetsData),), # Time Trial
        13: ((237, PacketMotionExData),), # Event
        14: ((101, PacketTimeTrialData),), # Car Damage (Full)
    }

