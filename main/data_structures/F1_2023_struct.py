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
        ("m_worldPositionX",        DataTypes.FLOAT.value),         # World space X position - metres
        ("m_worldPositionY",        DataTypes.FLOAT.value),         # World space Y position
        ("m_worldPositionZ",        DataTypes.FLOAT.value),         # World space Z position
        ("m_worldVelocityX",        DataTypes.FLOAT.value),         # Velocity in world space X – metres/s
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


### Session Packet -- 2 per second -- 644 bytes


class MarshalZone(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (45 instead of at least 52 bytes)
    _fields_ = [
        ("m_zoneStart", DataTypes.FLOAT.value),         # Fraction (0..1) of way through the lap the marshal zone starts
        ("m_zoneFlag",  DataTypes.SIGNED_INT8.value),   # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow
    ]


class WeatherForecastSample(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (753 instead of at least 828 bytes)
    _fields_ = [
        ("m_sessionType",               DataTypes.UNSIGNED_INT8.value), # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
        ("m_timeOffset",                DataTypes.UNSIGNED_INT8.value), # Time in minutes the forecast is for
        ("m_weather",                   DataTypes.UNSIGNED_INT8.value), # Weather - 0 = clear, 1 = light cloud, 2 = overcast, 3 = light rain, 4 = heavy rain, 5 = storm
        ("m_trackTemperature",          DataTypes.SIGNED_INT8.value),   # Track temp. in degrees Celsius
        ("m_trackTemperatureChange",    DataTypes.SIGNED_INT8.value),   # Track temp. change – 0 = up, 1 = down, 2 = no change
        ("m_airTemperature",            DataTypes.SIGNED_INT8.value),   # Air temp. in degrees celsius
        ("m_airTemperatureChange",      DataTypes.SIGNED_INT8.value),   # Air temp. change – 0 = up, 1 = down, 2 = no change
        ("m_rainPercentage",            DataTypes.UNSIGNED_INT8.value), # Rain percentage (0-100)
    ]


class PacketSessionData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (753 instead of at least 828 bytes)
    _fields_ = [
        ("m_header",                            PacketHeader),                          # Header
        ("m_weather",                           DataTypes.UNSIGNED_INT8.value),         # Weather - 0 = clear, 1 = light cloud, 2 = overcast, 3 = light rain, 4 = heavy rain, 5 = storm
        ("m_trackTemperature",                  DataTypes.SIGNED_INT8.value),           # Track temp. in degrees celsius
        ("m_airTemperature",                    DataTypes.SIGNED_INT8.value),           # Air temp. in degrees celsius
        ("m_totalLaps",                         DataTypes.UNSIGNED_INT8.value),         # Total number of laps in this race
        ("m_trackLength",                       DataTypes.UNSIGNED_INT16.value),        # Track length in metres
        ("m_sessionType",                       DataTypes.UNSIGNED_INT8.value),         # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
        ("m_trackId",                           DataTypes.SIGNED_INT8.value),           # -1 for unknown, see appendix
        ("m_formula",                           DataTypes.UNSIGNED_INT8.value),         # Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2, 3 = F1 Generic, 4 = Beta, 5 = Supercars, 6 = Esports, 7 = F2 2021
        ("m_sessionTimeLeft",                   DataTypes.UNSIGNED_INT16.value),        # Time left in session in seconds
        ("m_sessionDuration",                   DataTypes.UNSIGNED_INT16.value),        # Session duration in seconds
        ("m_pitSpeedLimit",                     DataTypes.UNSIGNED_INT8.value),         # Pit speed limit in kilometres per hour
        ("m_gamePaused",                        DataTypes.UNSIGNED_INT8.value),         # Whether the game is paused – network game only
        ("m_isSpectating",                      DataTypes.UNSIGNED_INT8.value),         # Whether the player is spectating
        ("m_spectatorCarIndex",                 DataTypes.UNSIGNED_INT8.value),         # Index of the car being spectated
        ("m_sliProNativeSupport",               DataTypes.UNSIGNED_INT8.value),         # SLI Pro support, 0 = inactive, 1 = active
        ("m_numMarshalZones",                   DataTypes.UNSIGNED_INT8.value),         # Number of marshal zones to follow
        ("m_marshalZones",                      MarshalZone * 21),                      # List of marshal zones – max 21
        ("m_safetyCarStatus",                   DataTypes.UNSIGNED_INT8.value),         # 0 = no safety car, 1 = full, 2 = virtual, 3 = formation lap
        ("m_networkGame",                       DataTypes.UNSIGNED_INT8.value),         # 0 = offline, 1 = online
        ("m_numWeatherForecastSamples",         DataTypes.UNSIGNED_INT8.value),         # Number of weather samples to follow
        ("m_weatherForecastSamples",            WeatherForecastSample * 64),            # Array of weather forecast samples
        ("m_forecastAccuracy",                  DataTypes.UNSIGNED_INT8.value),         # 0 = Perfect, 1 = Approximate
        ("m_aiDifficulty",                      DataTypes.UNSIGNED_INT8.value),         # AI Difficulty rating – 0-110
        ("m_seasonLinkIdentifier",              DataTypes.UNSIGNED_INT32.value),        # Identifier for season - persists across saves
        ("m_weekendLinkIdentifier",             DataTypes.UNSIGNED_INT32.value),        # Identifier for weekend - persists across saves
        ("m_sessionLinkIdentifier",             DataTypes.UNSIGNED_INT32.value),        # Identifier for session - persists across saves
        ("m_pitStopWindowIdealLap",             DataTypes.UNSIGNED_INT8.value),         # Ideal lap to pit on for current strategy (player)
        ("m_pitStopWindowLatestLap",            DataTypes.UNSIGNED_INT8.value),         # Latest lap to pit on for current strategy (player)
        ("m_pitStopRejoinPosition",             DataTypes.UNSIGNED_INT8.value),         # Predicted position to rejoin at (player)
        ("m_steeringAssist",                    DataTypes.UNSIGNED_INT8.value),         # 0 = off, 1 = on
        ("m_brakingAssist",                     DataTypes.UNSIGNED_INT8.value),         # 0 = off, 1 = low, 2 = medium, 3 = high
        ("m_gearboxAssist",                     DataTypes.UNSIGNED_INT8.value),         # 1 = manual, 2 = manual & suggested gear, 3 = auto
        ("m_pitAssist",                         DataTypes.UNSIGNED_INT8.value),         # 0 = off, 1 = on
        ("m_pitReleaseAssist",                  DataTypes.UNSIGNED_INT8.value),         # 0 = off, 1 = on
        ("m_ersAssist",                         DataTypes.UNSIGNED_INT8.value),         # 0 = off, 1 = on
        ("m_drsAssist",                         DataTypes.UNSIGNED_INT8.value),         # 0 = off, 1 = on
        ("m_dynamicRacingLine",                 DataTypes.UNSIGNED_INT8.value),         # 0 = off, 1 = corners only, 2 = full
        ("m_dynamicRacingLineType",             DataTypes.UNSIGNED_INT8.value),         # 0 = 2D, 1 = 3D
        ("m_gameMode",                          DataTypes.UNSIGNED_INT8.value),         # Game mode id - see appendix
        ("m_ruleSet",                           DataTypes.UNSIGNED_INT8.value),         # Ruleset - see appendix
        ("m_timeOfDay",                         DataTypes.UNSIGNED_INT32.value),        # Local time of day - minutes since midnight
        ("m_sessionLength",                     DataTypes.UNSIGNED_INT8.value),         # 0 = None, 2 = Very Short, 3 = Short, 4 = Medium, 5 = Medium Long, 6 = Long, 7 = Full
        ("m_speedUnitsLeadPlayer",              DataTypes.UNSIGNED_INT8.value),         # 0 = MPH, 1 = KPH
        ("m_temperatureUnitsLeadPlayer",        DataTypes.UNSIGNED_INT8.value),         # 0 = Celsius, 1 = Fahrenheit
        ("m_speedUnitsSecondaryPlayer",         DataTypes.UNSIGNED_INT8.value),         # 0 = MPH, 1 = KPH
        ("m_temperatureUnitsSecondaryPlayer",   DataTypes.UNSIGNED_INT8.value),         # 0 = Celsius, 1 = Fahrenheit
        ("m_numSafetyCarPeriods",               DataTypes.UNSIGNED_INT8.value),         # Number of safety cars called during session
        ("m_numVirtualSafetyCarPeriods",        DataTypes.UNSIGNED_INT8.value),         # Number of virtual safety cars called
        ("m_numRedFlagPeriods",                 DataTypes.UNSIGNED_INT8.value),         # Number of red flags called during session
    ]


### Lap Data Packet -- Rate as specified in menus -- 1131 bytes


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
        ("m_deltaToRaceLeaderMSPart",       DataTypes.UNSIGNED_INT16.value),    # Time delta to race leader milliseconds part
        ("m_lapDistance",                   DataTypes.FLOAT.value),             # Distance vehicle is around current lap in metres - can, be negative if line not crossed yet
        ("m_totalDistance",                 DataTypes.FLOAT.value),             # Total distance travelled in session in metres - can, be negative if line not crossed yet
        ("m_safetyCarDelta",                DataTypes.FLOAT.value),             # Delta in seconds for safety car
        ("m_carPosition",                   DataTypes.UNSIGNED_INT8.value),     # Car race position
        ("m_currentLapNum",                 DataTypes.UNSIGNED_INT8.value),     # Current lap number
        ("m_pitStatus",                     DataTypes.UNSIGNED_INT8.value),     # 0 = none, 1 = pitting, 2 = in pit area
        ("m_numPitStops",                   DataTypes.UNSIGNED_INT8.value),     # Number of pit stops taken in this race
        ("m_sector",                        DataTypes.UNSIGNED_INT8.value),     # 0 = sector1, 1 = sector2, 2 = sector3
        ("m_currentLapInvalid",             DataTypes.UNSIGNED_INT8.value),     # Current lap invalid - 0 = valid, 1 = invalid
        ("m_penalties",                     DataTypes.UNSIGNED_INT8.value),     # Accumulated time penalties in seconds to be added
        ("m_totalWarnings",                 DataTypes.UNSIGNED_INT8.value),     # Accumulated number of warnings issued
        ("m_cornerCuttingWarnings",         DataTypes.UNSIGNED_INT8.value),     # Accumulated number of corners cutting warnings issued
        ("m_numUnservedDriveThroughPens",   DataTypes.UNSIGNED_INT8.value),     # Num drive through pens left to serve
        ("m_numUnservedStopGoPens",         DataTypes.UNSIGNED_INT8.value),     # Num stop go pens left to serve
        ("m_gridPosition",                  DataTypes.UNSIGNED_INT8.value),     # Grid position the vehicle started the race in
        ("m_driverStatus",                  DataTypes.UNSIGNED_INT8.value),     # Status of driver - 0 = in garage, 1 = flying lap, 2 = in lap, 3 = out lap, 4 = on track
        ("m_resultStatus",                  DataTypes.UNSIGNED_INT8.value),     # Result status - 0 = invalid, 1 = inactive, 2 = active, 3 = finished, 4 = didnotfinish, 5 = disqualified, 6 = not classified, 7 = retired
        ("m_pitLaneTimerActive",            DataTypes.UNSIGNED_INT8.value),     # Pit lane timing, 0 = inactive, 1 = active
        ("m_pitLaneTimeInLaneInMs",         DataTypes.UNSIGNED_INT16.value),    # If active, the current time spent in the pit lane in ms
        ("m_pitStopTimerInMs",              DataTypes.UNSIGNED_INT16.value),    # Time of the actual pit stop in ms
        ("m_pitStopShouldServePen",         DataTypes.UNSIGNED_INT8.value),     # Whether the car should serve a penalty at this stop
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
        ("penaltyType",         DataTypes.UNSIGNED_INT8.value), # Penalty type – see Appendices
        ("infringementType",    DataTypes.UNSIGNED_INT8.value), # Infringement type – see Appendices
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
        ("isOverallFastestInSession",   DataTypes.UNSIGNED_INT8.value),     # Overall fastest speed in session = 1, otherwise 0
        ("isDriverFastestInSession",    DataTypes.UNSIGNED_INT8.value),     # Fastest speed for driver in session = 1, otherwise 0
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
        ("m_buttonStatus",  DataTypes.UNSIGNED_INT32.value),    # Bit flags specifying which buttons are being pressed currently - see appendices
    ]


class Overtake(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("overtakingVehicleIdx",        DataTypes.UNSIGNED_INT8.value), # Vehicle index of the vehicle overtaking
        ("beingOvertakenVehicleIdx",    DataTypes.UNSIGNED_INT8.value), # Vehicle index of the vehicle being overtaken
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
    ]


class PacketEventData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (45 instead of at least 52 bytes)
    _fields_ = [
        ("m_header",            PacketHeader),                      # Header
        ("m_eventStringCode",   DataTypes.UNSIGNED_INT8.value * 4), # Event string code
        ("m_eventDetails",      EventDataDetails),                  # Event details - should be interpreted differently for each type
    ]


### Participants Packet -- Every 5 seconds -- 1306 bytes


class ParticipantData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1350 instead of at least 1394 bytes)
    _fields_ = [
        ("m_aiControlled",      DataTypes.UNSIGNED_INT8.value),     # Whether the vehicle is AI (1) or Human (0) controlled
        ("m_driverId",          DataTypes.UNSIGNED_INT8.value),     # Driver id - see appendix, 255 if network human
        ("m_networkId",         DataTypes.UNSIGNED_INT8.value),     # Network id – unique identifier for network players
        ("m_teamId",            DataTypes.UNSIGNED_INT8.value),     # Team id - see appendix
        ("m_myTeam",            DataTypes.UNSIGNED_INT8.value),     # My team flag – 1 = My Team, 0 = otherwise
        ("m_raceNumber",        DataTypes.UNSIGNED_INT8.value),     # Race number of the car
        ("m_nationality",       DataTypes.UNSIGNED_INT8.value),     # Nationality of the driver
        ("m_name",              DataTypes.CHAR.value * 48),         # Name of participant in UTF-8 format – null terminated, Will be truncated with … (U+2026) if too long
        ("m_yourTelemetry",     DataTypes.UNSIGNED_INT8.value),     # The player's UDP setting, 0 = restricted, 1 = public
        ("m_showOnlineNames",   DataTypes.UNSIGNED_INT8.value),     # The player's show online names setting, 0 = off, 1 = on
        ("m_platform",          DataTypes.UNSIGNED_INT8.value),     # 1 = Steam, 3 = PlayStation, 4 = Xbox, 6 = Origin, 255 = unknown
    ]


class PacketParticipantsData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1350 instead of at least 1394 bytes)
    _fields_ = [
        ("m_header",            PacketHeader),                      # Header
        ("m_numActiveCars",     DataTypes.UNSIGNED_INT8.value),     # Number of active cars in the data – should match number of cars on HUD
        ("m_participants",      ParticipantData * 22),
    ]


### Car Setups Packet -- 2 per second -- 1107 bytes


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
        ("m_drs",                       DataTypes.UNSIGNED_INT8.value),         # 0 = off, 1 = on
        ("m_revLightsPercent",          DataTypes.UNSIGNED_INT8.value),         # Rev lights indicator (percentage)
        ("m_revLightsBitValue",         DataTypes.UNSIGNED_INT16.value),        # Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
        ("m_brakesTemperature",         DataTypes.UNSIGNED_INT16.value * 4),    # Brakes temperature (celsius)
        ("m_tyresSurfaceTemperature",   DataTypes.UNSIGNED_INT8.value * 4),     # Tyres surface temperature (celsius)
        ("m_tyresInnerTemperature",     DataTypes.UNSIGNED_INT8.value * 4),     # Tyres inner temperature (celsius)
        ("m_engineTemperature",         DataTypes.UNSIGNED_INT16.value),        # Engine temperature (celsius)
        ("m_tyresPressure",             DataTypes.FLOAT.value * 4),             # Tyres pressure (PSI)
        ("m_surfaceType",               DataTypes.UNSIGNED_INT8.value * 4),     # Driving surface, see appendices
    ]


class PacketCarTelemetryData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1352 instead of at least 1444 bytes)
    _fields_ = [
        ("m_header",                        PacketHeader),                      # Header
        ("m_carTelemetryData",              CarTelemetryData * 22),
        ("m_mfdPanelIndex",                 DataTypes.UNSIGNED_INT8.value),     # Index of MFD panel open - 255 = MFD closed, Single player, race – 0 = Car setup, 1 = Pits, 2 = Damage, 3 =  Engine, 4 = Temperatures - May vary depending on game mode
        ("m_mfdPanelIndexSecondaryPlayer",  DataTypes.UNSIGNED_INT8.value),     # See above
        ("m_suggestedGear",                 DataTypes.SIGNED_INT8.value),       # Suggested gear for the player (1-8), 0 if no gear suggested
    ]


### Car Status Packet -- Rate as specified in menus -- 1239 bytes


class CarStatusData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1239 instead of at least 1440 bytes)
    _fields_ = [
        ("m_tractionControl",           DataTypes.UNSIGNED_INT8.value),     # Traction control - 0 = off, 1 = medium, 2 = full
        ("m_antiLockBrakes",            DataTypes.UNSIGNED_INT8.value),     # 0 (off) - 1 (on)
        ("m_fuelMix",                   DataTypes.UNSIGNED_INT8.value),     # Fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
        ("m_frontBrakeBias",            DataTypes.UNSIGNED_INT8.value),     # Front brake bias (percentage)
        ("m_pitLimiterStatus",          DataTypes.UNSIGNED_INT8.value),     # Pit limiter status - 0 = off, 1 = on
        ("m_fuelInTank",                DataTypes.FLOAT.value),             # Current fuel mass
        ("m_fuelCapacity",              DataTypes.FLOAT.value),             # Fuel capacity
        ("m_fuelRemainingLaps",         DataTypes.FLOAT.value),             # Fuel remaining in terms of laps (value on MFD)
        ("m_maxRpm",                    DataTypes.UNSIGNED_INT16.value),    # Cars max RPM, point of rev limiter
        ("m_idleRpm",                   DataTypes.UNSIGNED_INT16.value),    # Cars idle RPM
        ("m_maxGears",                  DataTypes.UNSIGNED_INT8.value),     # Maximum number of gears
        ("m_drsAllowed",                DataTypes.UNSIGNED_INT8.value),     # 0 = not allowed, 1 = allowed
        ("m_drsActivationDistance",     DataTypes.UNSIGNED_INT16.value),    # 0 = DRS not available, non-zero - DRS will be available in [X] metres
        ("m_actualTyreCompound",        DataTypes.UNSIGNED_INT8.value),     # F1 Modern - 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1, 21 = C0, 7 = inter, 8 = wet
                                                                            # F1 Classic - 9 = dry, 10 = wet
                                                                            # F2 – 11 = super soft, 12 = soft, 13 = medium, 14 = hard, 15 = wet
        ("m_visualTyreCompound",        DataTypes.UNSIGNED_INT8.value),     # F1 visual (can be different from actual compound) - 16 = soft, 17 = medium, 18 = hard, 7 = inter, 8 = wet
                                                                            # F1 Classic – same as above
                                                                            # F2 ‘19, 15 = wet, 19 – super soft, 20 = soft, 21 = medium , 22 = hard
        ("m_tyresAgeLaps",              DataTypes.UNSIGNED_INT8.value),     # Age in laps of the current set of tyres
        ("m_vehicleFiaFlags",           DataTypes.SIGNED_INT8.value),       # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow
        ("m_enginePowerICE",            DataTypes.FLOAT.value),             # Engine power output of ICE (W)
        ("m_enginePowerMGUK",           DataTypes.FLOAT.value),             # Engine power output of MGU-K (W)
        ("m_ersStoreEnergy",            DataTypes.FLOAT.value),             # ERS energy store in Joules
        ("m_ersDeployMode",             DataTypes.UNSIGNED_INT8.value),     # ERS deployment mode, 0 = none, 1 = medium, 2 = hotlap, 3 = overtake
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
        ("m_resultStatus",      DataTypes.UNSIGNED_INT8.value),         # Result status - 0 = invalid, 1 = inactive, 2 = active, 3 = finished, 4 = didnotfinish, 5 = disqualified, 6 = not classified, 7 = retired
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


### Lobby Info Packet -- Two every second when in the lobby -- 1218 bytes


class LobbyInfoData(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("m_aiControlled",      DataTypes.UNSIGNED_INT8.value),     # Whether the vehicle is AI (1) or Human (0) controlled
        ("m_teamId",            DataTypes.UNSIGNED_INT8.value),     # Team id - see appendix (255 if no team currently selected)
        ("m_nationality",       DataTypes.UNSIGNED_INT8.value),     # Nationality of the driver
        ("m_platform",          DataTypes.UNSIGNED_INT8.value),     # 1 = Steam, 3 = PlayStation, 4 = Xbox, 6 = Origin, 255 = unknown
        ("m_name",              DataTypes.CHAR.value * 48),         # Name of participant in UTF-8 format – null terminated Will be truncated with ... (U+2026) if too long
        ("m_carNumber",         DataTypes.UNSIGNED_INT8.value),     # Car number of the player
        ("m_readyStatus",       DataTypes.UNSIGNED_INT8.value),     # 0 = not ready, 1 = ready, 2 = spectating
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
        ("m_drsFault",              DataTypes.UNSIGNED_INT8.value),         # Indicator for DRS fault, 0 = OK, 1 = fault
        ("m_ersFault",              DataTypes.UNSIGNED_INT8.value),         # Indicator for ERS fault, 0 = OK, 1 = fault
        ("m_gearBoxDamage",         DataTypes.UNSIGNED_INT8.value),         # Gear box damage (percentage)
        ("m_engineDamage",          DataTypes.UNSIGNED_INT8.value),         # Engine damage (percentage)
        ("m_engineMGUHWear",        DataTypes.UNSIGNED_INT8.value),         # Engine wear MGU-H (percentage)
        ("m_engineESWear",          DataTypes.UNSIGNED_INT8.value),         # Engine wear ES (percentage)
        ("m_engineCEWear",          DataTypes.UNSIGNED_INT8.value),         # Engine wear CE (percentage)
        ("m_engineICEWear",         DataTypes.UNSIGNED_INT8.value),         # Engine wear ICE (percentage)
        ("m_engineMGUKWear",        DataTypes.UNSIGNED_INT8.value),         # Engine wear MGU-K (percentage)
        ("m_engineTCWear",          DataTypes.UNSIGNED_INT8.value),         # Engine wear TC (percentage)
        ("m_engineBlown",           DataTypes.UNSIGNED_INT8.value),         # Engine blown, 0 = OK, 1 = fault
        ("m_engineSeized",          DataTypes.UNSIGNED_INT8.value),         # Engine seized, 0 = OK, 1 = fault
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
        ("m_lapValidBitFlags",      DataTypes.UNSIGNED_INT8.value),     # 0x01 bit set-lap valid, 0x02 bit set-sector 1 valid, 0x04 bit set-sector 2 valid, 0x08 bit set-sector 3 valid
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
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",        PacketHeader),                      # Header
        ("m_carIdx",        DataTypes.UNSIGNED_INT8.value),     # Index of the car this data relates to
        ("m_tyreSetData",   TyreSetData * 20),                  # 13 (dry) + 7 (wet)
        ("m_fittedIdx",     DataTypes.UNSIGNED_INT8.value),     # Index into array of fitted tyre
    ]


### Motion Ex Packet -- Rate as specified in menus -- 217 bytes


class PacketMotionExData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
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
        ("m_angularVelocityX",          DataTypes.FLOAT.value),         # Angular velocity x-component – radians/s
        ("m_angularVelocityY",          DataTypes.FLOAT.value),         # Angular velocity y-component
        ("m_angularVelocityZ",          DataTypes.FLOAT.value),         # Angular velocity z-component
        ("m_angularAccelerationX",      DataTypes.FLOAT.value),         # Angular acceleration x-component – radians/s
        ("m_angularAccelerationY",      DataTypes.FLOAT.value),         # Angular acceleration y-component
        ("m_angularAccelerationZ",      DataTypes.FLOAT.value),         # Angular acceleration z-component
        ("m_frontWheelsAngle",          DataTypes.FLOAT.value),         # Current front wheels angle in radians
        ("m_wheelVertForce",            DataTypes.FLOAT.value * 4),     # Vertical forces for each wheel
    ]


### MetaData

class MetaData:
    # standard network info
    port: int = 20777
    fullBufferSize: int = 1460
    
    # use if a heartbeat is needed
    heartBeatPort = None
    heartBeatFunc = None
    
    # use for itinial hand shake
    handShakePort = None
    handShakeFunc = None
    
    # use if the data needs decrypting
    decrytionFunc = None
    
    # use if there is a header packet
    headerInfo: tuple[int, type] = (32, PacketHeader)
    packetIDAttribute: str = "m_packetId"
    
    # standard packet info
    packetInfo: dict[int, tuple[tuple[int, type], ...]] = {
        0: ((1349, PacketMotionData),),                 # Contains all motion data for player’s car – only sent while player is in control
        1: ((644, PacketSessionData),),                 # Data about the session – track, time left
        2: ((1131, PacketLapData),),                    # Data about all the lap times of cars in the session
        3: ((45, PacketEventData),),                    # Various notable events that happen during a session
        4: ((1306, PacketParticipantsData),),           # List of participants in the session, mostly relevant for multiplayer
        5: ((1107, PacketCarSetupData),),               # Packet detailing car setups for cars in the race
        6: ((1352, PacketCarTelemetryData),),           # Telemetry data for all cars
        7: ((1239, PacketCarStatusData),),              # Status data for all cars
        8: ((1020, PacketFinalClassificationData),),    # Final classification confirmation at the end of a race
        9: ((1218, PacketLobbyInfoData),),              # Information about players in a multiplayer lobby
        10: ((953, PacketCarDamageData),),              # Damage status for all cars
        11: ((1460, PacketSessionHistoryData),),        # Lap and tyre data for session
        12: ((231, PacketTyreSetsData),),               # Extended tyre set data
        13: ((217, PacketMotionExData),),               # Extended motion data for player car
    }

