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


### Packet Header -- 27 bytes


class PacketHeader(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_packetFormat",              DataTypes.UNSIGNED_INT16.value),    # 2020
        ("m_gameMajorVersion",          DataTypes.UNSIGNED_INT8.value),     # Game major version - "X.00"
        ("m_gameMinorVersion",          DataTypes.UNSIGNED_INT8.value),     # Game minor version - "1.XX"
        ("m_packetVersion",             DataTypes.UNSIGNED_INT8.value),     # Version of this packet type, all start from 1
        ("m_packetId",                  DataTypes.UNSIGNED_INT8.value),     # Identifier for the packet type, see below
        ("m_sessionUID",                DataTypes.UNSIGNED_INT64.value),    # Unique identifier for the session
        ("m_sessionTime",               DataTypes.FLOAT.value),             # Session timestamp
        ("m_frameIdentifier",           DataTypes.UNSIGNED_INT32.value),    # Identifier for the frame the data was retrieved on
        ("m_playerCarIndex",            DataTypes.UNSIGNED_INT8.value),     # Index of player's car in the array
        ("m_secondaryPlayerCarIndex",   DataTypes.UNSIGNED_INT8.value),     # Index of secondary player's car in the array (splitscreen), 255 if no second player
    ]


### Motion Packet -- Rate as specified in menus -- 1464 bytes


class CarMotionData(DataTypes.STRUCTURE.value):
    # _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
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
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carMotionData", CarMotionData * 22),    # Data for all cars on track
        # Extra player car ONLY data
        ("m_suspensionPosition",        DataTypes.FLOAT.value * 4),     # Note: All wheel arrays have the following order:
        ("m_suspensionVelocity",        DataTypes.FLOAT.value * 4),     # RL, RR, FL, FR
        ("m_suspensionAcceleration",    DataTypes.FLOAT.value * 4),     # RL, RR, FL, FR
        ("m_wheelSpeed",                DataTypes.FLOAT.value * 4),     # Speed of each wheel
        ("m_wheelSlip",                 DataTypes.FLOAT.value * 4),     # Slip ratio for each wheel
        ("m_localVelocityX",            DataTypes.FLOAT.value),         # Velocity in local space
        ("m_localVelocityY",            DataTypes.FLOAT.value),         # Velocity in local space
        ("m_localVelocityZ",            DataTypes.FLOAT.value),         # Velocity in local space
        ("m_angularVelocityX",          DataTypes.FLOAT.value),         # Angular velocity x-component
        ("m_angularVelocityY",          DataTypes.FLOAT.value),         # Angular velocity y-component
        ("m_angularVelocityZ",          DataTypes.FLOAT.value),         # Angular velocity z-component
        ("m_angularAccelerationX",      DataTypes.FLOAT.value),         # Angular acceleration x-component
        ("m_angularAccelerationY",      DataTypes.FLOAT.value),         # Angular acceleration y-component
        ("m_angularAccelerationZ",      DataTypes.FLOAT.value),         # Angular acceleration z-component
        ("m_frontWheelsAngle",          DataTypes.FLOAT.value),         # Current front wheels angle in radians
    ]


### Session Packet -- 2 per second -- 251 bytes


class MarshalZone(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_zoneStart", DataTypes.FLOAT.value),         # Fraction (0..1) of way through the lap the marshal zone starts
        ("m_zoneFlag",  DataTypes.SIGNED_INT8.value),   # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
    ]


class WeatherForecastSample(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_sessionType",               DataTypes.UNSIGNED_INT8.value), # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
        ("m_timeOffset",                DataTypes.UNSIGNED_INT8.value), # Time in minutes the forecast is for
        ("m_weather",                   DataTypes.UNSIGNED_INT8.value), # Weather - 0 = clear, 1 = light cloud, 2 = overcast, 3 = light rain, 4 = heavy rain, 5 = storm
        ("m_trackTemperature",          DataTypes.SIGNED_INT8.value),   # Track temp. in degrees Celsius
        ("m_airTemperature",            DataTypes.SIGNED_INT8.value),   # Air temp. in degrees celsius
    ]


class PacketSessionData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
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
        ("m_weatherForecastSamples",            WeatherForecastSample * 20),            # Array of weather forecast samples
    ]


### Lap Data Packet -- Rate as specified in menus -- 1190 bytes


class LapData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_lastLapTime",                   DataTypes.FLOAT.value),             # Last lap time in seconds
        ("m_currentLapTime",                DataTypes.FLOAT.value),             # Current time around the lap in seconds
        ("m_sector1TimeInMs",               DataTypes.UNSIGNED_INT16.value),    # Sector 1 time in milliseconds
        ("m_sector2TimeInMs",               DataTypes.UNSIGNED_INT16.value),    # Sector 2 time in milliseconds
        ("m_bestLapTime",                   DataTypes.FLOAT.value),             # Best lap time of the session in seconds
        ("m_bestLapNum",                    DataTypes.UNSIGNED_INT8.value),     # Lap number best time achieved on
        ("m_bestLapSector1TimeInMS",        DataTypes.UNSIGNED_INT16.value),    # Sector 1 time of best lap in the session in milliseconds
        ("m_bestLapSector2TimeInMS",        DataTypes.UNSIGNED_INT16.value),    # Sector 2 time of best lap in the session in milliseconds
        ("m_bestLapSector3TimeInMS",        DataTypes.UNSIGNED_INT16.value),    # Sector 3 time of best lap in the session in milliseconds
        ("m_bestOverallSector1TimeInMS",    DataTypes.UNSIGNED_INT16.value),    # Best overall sector 1 time of the session in milliseconds
        ("m_bestOverallSector1LapNum",      DataTypes.UNSIGNED_INT8.value),     # Lap number best overall sector 1 time achieved on
        ("m_bestOverallSector2TimeInMS",    DataTypes.UNSIGNED_INT16.value),    # Best overall sector 2 time of the session in milliseconds
        ("m_bestOverallSector2LapNum",      DataTypes.UNSIGNED_INT8.value),     # Lap number best overall sector 2 time achieved on
        ("m_bestOverallSector3TimeInMS",    DataTypes.UNSIGNED_INT16.value),    # Best overall sector 3 time of the session in milliseconds
        ("m_bestOverallSector3LapNum",      DataTypes.UNSIGNED_INT8.value),     # Lap number best overall sector 3 time achieved on
        ("m_lapDistance",                   DataTypes.FLOAT.value),             # Distance vehicle is around current lap in metres - can, be negative if line not crossed yet
        ("m_totalDistance",                 DataTypes.FLOAT.value),             # Total distance travelled in session in metres - can, be negative if line not crossed yet
        ("m_safetyCarDelta",                DataTypes.FLOAT.value),             # Delta in seconds for safety car
        ("m_carPosition",                   DataTypes.UNSIGNED_INT8.value),     # Car race position
        ("m_currentLapNum",                 DataTypes.UNSIGNED_INT8.value),     # Current lap number
        ("m_pitStatus",                     DataTypes.UNSIGNED_INT8.value),     # 0 = none, 1 = pitting, 2 = in pit area
        ("m_sector",                        DataTypes.UNSIGNED_INT8.value),     # 0 = sector1, 1 = sector2, 2 = sector3
        ("m_currentLapInvalid",             DataTypes.UNSIGNED_INT8.value),     # Current lap invalid - 0 = valid, 1 = invalid
        ("m_penalties",                     DataTypes.UNSIGNED_INT8.value),     # Accumulated time penalties in seconds to be added
        ("m_gridPosition",                  DataTypes.UNSIGNED_INT8.value),     # Grid position the vehicle started the race in
        ("m_driverStatus",                  DataTypes.UNSIGNED_INT8.value),     # Status of driver - 0 = in garage, 1 = flying lap, 2 = in lap, 3 = out lap, 4 = on track
        ("m_resultStatus",                  DataTypes.UNSIGNED_INT8.value),     # Result status - 0 = invalid, 1 = inactive, 2 = active, 3 = finished, 4 = didnotfinish, 5 = disqualified, 6 = not classified, 7 = retired
    ]


class PacketLapData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                PacketHeader),                      # Header
        ("m_lapData",               LapData * 22),                      # Lap data for all cars on track
    ]


### Event Packet -- When the event occurs -- 35 bytes


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
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("vehicleIdx",      DataTypes.UNSIGNED_INT8.value),     # Vehicle index of the vehicle triggering speed trap
        ("speed",           DataTypes.FLOAT.value),             # Top speed achieved in kilometres per hour
    ]


class EventDataDetails(DataTypes.UNION.value):
    _fields_ = [
        ("m_fastestLap",        FastestLap),
        ("m_retirement",        Retirement),
        ("m_teamMateInPits",    TeamMateInPits),
        ("m_raceWinner",        RaceWinner),
        ("m_penalty",           Penalty),
        ("m_speedTrap",         SpeedTrap),
    ]


class PacketEventData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",            PacketHeader),                      # Header
        ("m_eventStringCode",   DataTypes.UNSIGNED_INT8.value * 4), # Event string code
        ("m_eventDetails",      EventDataDetails),                  # Event details - should be interpreted differently for each type
    ]


### Participants Packet -- Every 5 seconds -- 1213 bytes


class ParticipantData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_aiControlled",      DataTypes.UNSIGNED_INT8.value),     # Whether the vehicle is AI (1) or Human (0) controlled
        ("m_driverId",          DataTypes.UNSIGNED_INT8.value),     # Driver id - see appendix, 255 if network human
        ("m_teamId",            DataTypes.UNSIGNED_INT8.value),     # Team id - see appendix
        ("m_raceNumber",        DataTypes.UNSIGNED_INT8.value),     # Race number of the car
        ("m_nationality",       DataTypes.UNSIGNED_INT8.value),     # Nationality of the driver
        ("m_name",              DataTypes.CHAR.value * 48),         # Name of participant in UTF-8 format – null terminated, Will be truncated with … (U+2026) if too long
        ("m_yourTelemetry",     DataTypes.UNSIGNED_INT8.value),     # The player's UDP setting, 0 = restricted, 1 = public
    ]


class PacketParticipantsData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",            PacketHeader),                      # Header
        ("m_numActiveCars",     DataTypes.UNSIGNED_INT8.value),     # Number of active cars in the data – should match number of cars on HUD
        ("m_participants",      ParticipantData * 22),
    ]


### Car Setups Packet -- 2 per second -- 1102 bytes


class CarSetupData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
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
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                PacketHeader),              # Header
        ("m_car_setups",            CarSetupData * 22),
    ]


### Car Telemetry Packet -- Rate as specified in menus -- 1307 bytes


class CarTelemetryData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
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
        ("m_brakesTemperature",         DataTypes.UNSIGNED_INT16.value * 4),    # Brakes temperature (celsius)
        ("m_tyresSurfaceTemperature",   DataTypes.UNSIGNED_INT8.value * 4),     # Tyres surface temperature (celsius)
        ("m_tyresInnerTemperature",     DataTypes.UNSIGNED_INT8.value * 4),     # Tyres inner temperature (celsius)
        ("m_engineTemperature",         DataTypes.UNSIGNED_INT16.value),        # Engine temperature (celsius)
        ("m_tyresPressure",             DataTypes.FLOAT.value * 4),             # Tyres pressure (PSI)
        ("m_surfaceType",               DataTypes.UNSIGNED_INT8.value * 4),     # Driving surface, see appendices
    ]


class PacketCarTelemetryData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                        PacketHeader),                      # Header
        ("m_carTelemetryData",              CarTelemetryData * 22),
        ("m_buttonStatus",                  DataTypes.UNSIGNED_INT32.value),    # Bit flags specifying which buttons are being pressed currently - see appendices
        ("m_mfdPanelIndex",                 DataTypes.UNSIGNED_INT8.value),     # Index of MFD panel open - 255 = MFD closed, Single player, race – 0 = Car setup, 1 = Pits, 2 = Damage, 3 =  Engine, 4 = Temperatures - May vary depending on game mode
        ("m_mfdPanelIndexSecondaryPlayer",  DataTypes.UNSIGNED_INT8.value),     # See above
        ("m_suggestedGear",                 DataTypes.SIGNED_INT8.value),       # Suggested gear for the player (1-8), 0 if no gear suggested
    ]


### Car Status Packet -- Rate as specified in menus -- 1344 bytes


class CarStatusData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
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
        ("m_tyresWear",                 DataTypes.UNSIGNED_INT8.value * 4), # Tyre wear percentage
        ("m_actualTyreCompound",        DataTypes.UNSIGNED_INT8.value),     # F1 Modern - 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1, 21 = C0, 7 = inter, 8 = wet
                                                                            # F1 Classic - 9 = dry, 10 = wet
                                                                            # F2 – 11 = super soft, 12 = soft, 13 = medium, 14 = hard, 15 = wet
        ("m_visualTyreCompound",        DataTypes.UNSIGNED_INT8.value),     # F1 visual (can be different from actual compound) - 16 = soft, 17 = medium, 18 = hard, 7 = inter, 8 = wet
                                                                            # F1 Classic – same as above
                                                                            # F2 ‘19, 15 = wet, 19 – super soft, 20 = soft, 21 = medium , 22 = hard
        ("m_tyresAgeLaps",              DataTypes.UNSIGNED_INT8.value),     # Age in laps of the current set of tyres
        ("m_tyresDamage",               DataTypes.UNSIGNED_INT8.value * 4), # Tyre damage (percentage)
        ("m_frontLeftWingDamage",       DataTypes.SIGNED_INT8.value),       # Front left wing damage (percentage)
        ("m_frontRightWingDamage",      DataTypes.SIGNED_INT8.value),       # Front right wing damage (percentage)
        ("m_rearWingDamage",            DataTypes.SIGNED_INT8.value),       # Rear wing damage (percentage)
        ("m_drsFault",                  DataTypes.SIGNED_INT8.value),       # Indicator for DRS fault, 0 = OK, 1 = fault
        ("m_engineDamage",              DataTypes.SIGNED_INT8.value),       # Engine damage (percentage)
        ("m_gearBoxDamage",             DataTypes.SIGNED_INT8.value),       # Gear box damage (percentage)
        ("m_vehicleFiaFlags",           DataTypes.SIGNED_INT8.value),       # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow
        ("m_ersStoreEnergy",            DataTypes.FLOAT.value),             # ERS energy store in Joules
        ("m_ersDeployMode",             DataTypes.UNSIGNED_INT8.value),     # ERS deployment mode, 0 = none, 1 = medium, 2 = hotlap, 3 = overtake
        ("m_ersHarvestedThisLapMguk",   DataTypes.FLOAT.value),             # ERS energy harvested this lap by MGU-K
        ("m_ersHarvestedThisLapMguh",   DataTypes.FLOAT.value),             # ERS energy harvested this lap by MGU-H
        ("m_ersDeployedThisLap",        DataTypes.FLOAT.value),             # ERS energy deployed this lap
    ]


class PacketCarStatusData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carStatusData", CarStatusData * 22),
    ]


### Final Classification Packet -- Once at the end of a race -- 839 bytes


class FinalClassificationData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
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
    ]


class PacketFinalClassificationData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                PacketHeader),                      # Header
        ("m_numCars",               DataTypes.UNSIGNED_INT8.value),     # Number of cars in the final classification
        ("m_classificationData",    FinalClassificationData * 22),
    ]


### Lobby Info Packet -- Two every second when in the lobby -- 1169 bytes


class LobbyInfoData(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("m_aiControlled",      DataTypes.UNSIGNED_INT8.value),     # Whether the vehicle is AI (1) or Human (0) controlled
        ("m_teamId",            DataTypes.UNSIGNED_INT8.value),     # Team id - see appendix (255 if no team currently selected)
        ("m_nationality",       DataTypes.UNSIGNED_INT8.value),     # Nationality of the driver
        ("m_name",              DataTypes.CHAR.value * 48),         # Name of participant in UTF-8 format – null terminated Will be truncated with ... (U+2026) if too long
        ("m_readyStatus",       DataTypes.UNSIGNED_INT8.value),     # 0 = not ready, 1 = ready, 2 = spectating
    ]


class PacketLobbyInfoData(DataTypes.STRUCTURE.value):
    _fields_ = [
        ("m_header",        PacketHeader),                      # Header Packet specific data
        ("m_numPlayers",    DataTypes.UNSIGNED_INT8.value),     # Number of players in the lobby data
        ("m_lobbyPlayers",  LobbyInfoData * 22),
    ]


### MetaData

class MetaData:
    # standard network info
    port: int = 20777
    fullBufferSize: int = 1464
    
    # use if a heartbeat is needed
    heartBeatPort = None
    heartBeatFunc = None
    
    # use for itinial hand shake
    handShakePort = None
    handShakeFunc = None
    
    # use if the data needs decrypting
    decrytionFunc = None
    
    # use if there is a header packet
    headerInfo: tuple[int, type] = (27, PacketHeader)
    packetIDAttribute: str = "m_packetId"
    
    # standard packet info
    packetInfo: dict[int, tuple[tuple[int, type], ...]] = {
        0: ((1464, PacketMotionData),),                 # Contains all motion data for player’s car – only sent while player is in control
        1: ((251, PacketSessionData),),                 # Data about the session – track, time left
        2: ((1190, PacketLapData),),                     # Data about all the lap times of cars in the session
        3: ((35, PacketEventData),),                    # Various notable events that happen during a session
        4: ((1213, PacketParticipantsData),),           # List of participants in the session, mostly relevant for multiplayer
        5: ((1102, PacketCarSetupData),),               # Packet detailing car setups for cars in the race
        6: ((1307, PacketCarTelemetryData),),           # Telemetry data for all cars
        7: ((1344, PacketCarStatusData),),              # Status data for all cars
        8: ((839, PacketFinalClassificationData),),     # Final classification confirmation at the end of a race
        9: ((1169, PacketLobbyInfoData),),              # Information about players in a multiplayer lobby
    }

