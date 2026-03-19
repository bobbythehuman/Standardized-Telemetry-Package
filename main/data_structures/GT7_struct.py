import ctypes
from enum import Enum

# source
# https://github.com/MacManley/gt7-udp

class DataTypes(Enum):
    STRUCTURE = ctypes.LittleEndianStructure
    
    SIGNED_INT = ctypes.c_int
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT16 = ctypes.c_int16
    SIGNED_INT32 = ctypes.c_int32
    
    UNSIGNED_INT = ctypes.c_uint
    UNSIGNED_INT8 = ctypes.c_uint8
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT32 = ctypes.c_uint32
    
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char


class PacketAData(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("magic",                       DataTypes.SIGNED_INT32.value),  # Magic, different value defines what game is being played
        ("position",                    DataTypes.FLOAT.value * 3),     # Position on Track in meters in each axis
        ("worldVelocity",               DataTypes.FLOAT.value * 3),     # Velocity in meters for each axis
        ("rotation",                    DataTypes.FLOAT.value * 3),     # Rotation (Pitch/Yaw/Roll) (RANGE: -1 -> 1)
        ("orientationRelativeToNorth",  DataTypes.FLOAT.value),         # Orientation to North (RANGE: 1.0 (North) -> 0.0 (South))
        ("angularVelocity",             DataTypes.FLOAT.value * 3),     # Speed at which the car turns around axis in rad/s (RANGE: -1 -> 1)
        ("bodyHeight",                  DataTypes.FLOAT.value),         # Body height
        ("EngineRPM",                   DataTypes.FLOAT.value),         # Engine revolutions per minute

        ("iv",              DataTypes.UNSIGNED_INT8.value * 4),     # IV for Salsa20 encryption/decryption
        ("fuelLevel",       DataTypes.FLOAT.value),                 # Fuel level of car in liters 
        ("fuelCapacity",    DataTypes.FLOAT.value),                 # Max fuel capacity for current car (RANGE: 100 (most cars) -> 5 (karts) -> 0 (electric cars))  
        ("speed",           DataTypes.FLOAT.value),                 # Speed in m/s
        ("boost",           DataTypes.FLOAT.value),                 # Offset by +1 (EXAMPLE: 1.0 = 0 X 100kPa, 2.0 = 1 x 100kPa) # TODO apply -1 offset (from original source)
        ("oilPressure",     DataTypes.FLOAT.value),                 # Oil pressure in bars
        ("waterTemp",       DataTypes.FLOAT.value),                 # Constantly 85
        ("oilTemp",         DataTypes.FLOAT.value),                 # Constantly 110
        ("tyreTemp",        DataTypes.FLOAT.value * 4),             # Tyre temp for all 4 tires (FL -> FR -> RL -> RR)
        
        ("packetId",            DataTypes.SIGNED_INT32.value),  # ID of packet
        ("lapCount",            DataTypes.SIGNED_INT16.value),  # Lap count
        ("totalLaps",           DataTypes.SIGNED_INT16.value),  # Laps to finish
        ("bestLaptime",         DataTypes.SIGNED_INT32.value),  # Best lap time, defaults to -1 if not set
        ("lastLaptime",         DataTypes.SIGNED_INT32.value),  # Previous lap time, defaults to -1 if not set
        ("dayProgression",      DataTypes.SIGNED_INT32.value),  # Current time of day on track in ms
        ("RaceStartPosition",   DataTypes.SIGNED_INT16.value),  # Position of the car before the start of the race, defaults to -1 after race start
        ("preRaceNumCars",      DataTypes.SIGNED_INT16.value),  # Number of cars before the race start, defaults to -1 after start of the race
        ("minAlertRPM",         DataTypes.SIGNED_INT16.value),  # Minimum RPM that the rev limiter displays an alert
        ("maxAlertRPM",         DataTypes.SIGNED_INT16.value),  # Maximum RPM that the rev limiter displays an alert
        ("calcMaxSpeed",        DataTypes.SIGNED_INT16.value),  # Highest possible speed achievable of the current transmission settings
        
        ("flags",           DataTypes.SIGNED_INT16.value), # Packet flags # TODO: Get working (from original source)
        
        ("gears",       DataTypes.UNSIGNED_INT8.value), # First 4 bits: Current Gear, Last 4 bits: Suggested Gear, # TODO see getCurrentGearFromByte and getSuggestedGearFromByte
        ("throttle",    DataTypes.UNSIGNED_INT8.value), # Throttle (RANGE: 0 -> 255)
        ("brake",       DataTypes.UNSIGNED_INT8.value), # Brake (RANGE: 0 -> 255)
        ("PADDING",     DataTypes.UNSIGNED_INT8.value), # Padding byte # * might not be needed
        
        ("roadPlane",               DataTypes.FLOAT.value * 3),     # Banking of the road
        ("roadPlaneDistance",       DataTypes.FLOAT.value),         # Distance above or below the plane, e.g a dip in the road is negative, hill is positive.
        ("wheelRPS",                DataTypes.FLOAT.value * 4),     # Revolutions per second of tyres in rads
        ("tyreRadius",              DataTypes.FLOAT.value * 4),     # Radius of the tyre in meters
        ("suspHeight",              DataTypes.FLOAT.value * 4),     # Suspension height of the car
        ("UNKNOWNFLOATS",           DataTypes.FLOAT.value * 8),     # Unknown float (from original source)
        ("clutch",                  DataTypes.FLOAT.value),         # Clutch (RANGE: 0.0 -> 1.0)
        ("clutchEngagement",        DataTypes.FLOAT.value),         # Clutch Engangement (RANGE: 0.0 -> 1.0)
        ("RPMFromClutchToGearbox",  DataTypes.FLOAT.value),         # Pretty much same as engine RPM, is 0 when clutch is depressed
        ("transmissionTopSpeed",    DataTypes.FLOAT.value),         # Top speed as gear ratio value
        ("gearRatios",              DataTypes.FLOAT.value  * 8),    # Gear ratios of the car up to 8
        ("carCode",                 DataTypes.SIGNED_INT32.value),  # This value may be overriden if using a car with more then 9 gears
    ]


class PacketBData(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("magic",                       DataTypes.SIGNED_INT32.value),  # Magic, different value defines what game is being played
        ("position",                    DataTypes.FLOAT.value * 3),     # Position on Track in meters in each axis
        ("worldVelocity",               DataTypes.FLOAT.value * 3),     # Velocity in meters for each axis
        ("rotation",                    DataTypes.FLOAT.value * 3),     # Rotation (Pitch/Yaw/Roll) (RANGE: -1 -> 1)
        ("orientationRelativeToNorth",  DataTypes.FLOAT.value),         # Orientation to North (RANGE: 1.0 (North) -> 0.0 (South))
        ("angularVelocity",             DataTypes.FLOAT.value * 3),     # Speed at which the car turns around axis in rad/s (RANGE: -1 -> 1)
        ("bodyHeight",                  DataTypes.FLOAT.value),         # Body height
        ("EngineRPM",                   DataTypes.FLOAT.value),         # Engine revolutions per minute

        ("iv",              DataTypes.UNSIGNED_INT8.value * 4),     # IV for Salsa20 encryption/decryption
        ("fuelLevel",       DataTypes.FLOAT.value),                 # Fuel level of car in liters 
        ("fuelCapacity",    DataTypes.FLOAT.value),                 # Max fuel capacity for current car (RANGE: 100 (most cars) -> 5 (karts) -> 0 (electric cars))  
        ("speed",           DataTypes.FLOAT.value),                 # Speed in m/s
        ("boost",           DataTypes.FLOAT.value),                 # Offset by +1 (EXAMPLE: 1.0 = 0 X 100kPa, 2.0 = 1 x 100kPa) # TODO apply -1 offset (from original source)
        ("oilPressure",     DataTypes.FLOAT.value),                 # Oil pressure in bars
        ("waterTemp",       DataTypes.FLOAT.value),                 # Constantly 85
        ("oilTemp",         DataTypes.FLOAT.value),                 # Constantly 110
        ("tyreTemp",        DataTypes.FLOAT.value * 4),             # Tyre temp for all 4 tires (FL -> FR -> RL -> RR)
        
        ("packetId",            DataTypes.SIGNED_INT32.value),  # ID of packet
        ("lapCount",            DataTypes.SIGNED_INT16.value),  # Lap count
        ("totalLaps",           DataTypes.SIGNED_INT16.value),  # Laps to finish
        ("bestLaptime",         DataTypes.SIGNED_INT32.value),  # Best lap time, defaults to -1 if not set
        ("lastLaptime",         DataTypes.SIGNED_INT32.value),  # Previous lap time, defaults to -1 if not set
        ("dayProgression",      DataTypes.SIGNED_INT32.value),  # Current time of day on track in ms
        ("RaceStartPosition",   DataTypes.SIGNED_INT16.value),  # Position of the car before the start of the race, defaults to -1 after race start
        ("preRaceNumCars",      DataTypes.SIGNED_INT16.value),  # Number of cars before the race start, defaults to -1 after start of the race
        ("minAlertRPM",         DataTypes.SIGNED_INT16.value),  # Minimum RPM that the rev limiter displays an alert
        ("maxAlertRPM",         DataTypes.SIGNED_INT16.value),  # Maximum RPM that the rev limiter displays an alert
        ("calcMaxSpeed",        DataTypes.SIGNED_INT16.value),  # Highest possible speed achievable of the current transmission settings
        
        ("flags",           DataTypes.SIGNED_INT16.value), # Packet flags # TODO: Get working (from original source)
        
        ("gears",       DataTypes.UNSIGNED_INT8.value), # First 4 bits: Current Gear, Last 4 bits: Suggested Gear, # TODO see getCurrentGearFromByte and getSuggestedGearFromByte
        ("throttle",    DataTypes.UNSIGNED_INT8.value), # Throttle (RANGE: 0 -> 255)
        ("brake",       DataTypes.UNSIGNED_INT8.value), # Brake (RANGE: 0 -> 255)
        ("PADDING",     DataTypes.UNSIGNED_INT8.value), # Padding byte # * might not be needed
        
        ("roadPlane",               DataTypes.FLOAT.value * 3),     # Banking of the road
        ("roadPlaneDistance",       DataTypes.FLOAT.value),         # Distance above or below the plane, e.g a dip in the road is negative, hill is positive.
        ("wheelRPS",                DataTypes.FLOAT.value * 4),     # Revolutions per second of tyres in rads
        ("tyreRadius",              DataTypes.FLOAT.value * 4),     # Radius of the tyre in meters
        ("suspHeight",              DataTypes.FLOAT.value * 4),     # Suspension height of the car
        ("UNKNOWNFLOATS",           DataTypes.FLOAT.value * 8),     # Unknown float (from original source)
        ("clutch",                  DataTypes.FLOAT.value),         # Clutch (RANGE: 0.0 -> 1.0)
        ("clutchEngagement",        DataTypes.FLOAT.value),         # Clutch Engangement (RANGE: 0.0 -> 1.0)
        ("RPMFromClutchToGearbox",  DataTypes.FLOAT.value),         # Pretty much same as engine RPM, is 0 when clutch is depressed
        ("transmissionTopSpeed",    DataTypes.FLOAT.value),         # Top speed as gear ratio value
        ("gearRatios",              DataTypes.FLOAT.value  * 8),    # Gear ratios of the car up to 8
        ("carCode",                 DataTypes.SIGNED_INT32.value),  # This value may be overriden if using a car with more then 9 gears
        
        ("wheelRotation",   DataTypes.FLOAT.value),  # Calculates the wheel rotation in radians
        ("UNKNOWNFLOAT10",  DataTypes.FLOAT.value),  # Unknown float
        ("sway",            DataTypes.FLOAT.value),  # X axis acceleration
        ("heave",           DataTypes.FLOAT.value),  # Y axis acceleration
        ("surge",           DataTypes.FLOAT.value),  # Z axis acceleration
        
    ]


class PacketTildaData(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("magic",                       DataTypes.SIGNED_INT32.value),  # Magic, different value defines what game is being played
        ("position",                    DataTypes.FLOAT.value * 3),     # Position on Track in meters in each axis
        ("worldVelocity",               DataTypes.FLOAT.value * 3),     # Velocity in meters for each axis
        ("rotation",                    DataTypes.FLOAT.value * 3),     # Rotation (Pitch/Yaw/Roll) (RANGE: -1 -> 1)
        ("orientationRelativeToNorth",  DataTypes.FLOAT.value),         # Orientation to North (RANGE: 1.0 (North) -> 0.0 (South))
        ("angularVelocity",             DataTypes.FLOAT.value * 3),     # Speed at which the car turns around axis in rad/s (RANGE: -1 -> 1)
        ("bodyHeight",                  DataTypes.FLOAT.value),         # Body height
        ("EngineRPM",                   DataTypes.FLOAT.value),         # Engine revolutions per minute

        ("iv",              DataTypes.UNSIGNED_INT8.value * 4),     # IV for Salsa20 encryption/decryption
        ("fuelLevel",       DataTypes.FLOAT.value),                 # Fuel level of car in liters 
        ("fuelCapacity",    DataTypes.FLOAT.value),                 # Max fuel capacity for current car (RANGE: 100 (most cars) -> 5 (karts) -> 0 (electric cars))  
        ("speed",           DataTypes.FLOAT.value),                 # Speed in m/s
        ("boost",           DataTypes.FLOAT.value),                 # Offset by +1 (EXAMPLE: 1.0 = 0 X 100kPa, 2.0 = 1 x 100kPa) # TODO apply -1 offset (from original source)
        ("oilPressure",     DataTypes.FLOAT.value),                 # Oil pressure in bars
        ("waterTemp",       DataTypes.FLOAT.value),                 # Constantly 85
        ("oilTemp",         DataTypes.FLOAT.value),                 # Constantly 110
        ("tyreTemp",        DataTypes.FLOAT.value * 4),             # Tyre temp for all 4 tires (FL -> FR -> RL -> RR)
        
        ("packetId",            DataTypes.SIGNED_INT32.value),  # ID of packet
        ("lapCount",            DataTypes.SIGNED_INT16.value),  # Lap count
        ("totalLaps",           DataTypes.SIGNED_INT16.value),  # Laps to finish
        ("bestLaptime",         DataTypes.SIGNED_INT32.value),  # Best lap time, defaults to -1 if not set
        ("lastLaptime",         DataTypes.SIGNED_INT32.value),  # Previous lap time, defaults to -1 if not set
        ("dayProgression",      DataTypes.SIGNED_INT32.value),  # Current time of day on track in ms
        ("RaceStartPosition",   DataTypes.SIGNED_INT16.value),  # Position of the car before the start of the race, defaults to -1 after race start
        ("preRaceNumCars",      DataTypes.SIGNED_INT16.value),  # Number of cars before the race start, defaults to -1 after start of the race
        ("minAlertRPM",         DataTypes.SIGNED_INT16.value),  # Minimum RPM that the rev limiter displays an alert
        ("maxAlertRPM",         DataTypes.SIGNED_INT16.value),  # Maximum RPM that the rev limiter displays an alert
        ("calcMaxSpeed",        DataTypes.SIGNED_INT16.value),  # Highest possible speed achievable of the current transmission settings
        
        ("flags",           DataTypes.SIGNED_INT16.value), # Packet flags # TODO: Get working (from original source)
        
        ("gears",       DataTypes.UNSIGNED_INT8.value), # First 4 bits: Current Gear, Last 4 bits: Suggested Gear, # TODO see getCurrentGearFromByte and getSuggestedGearFromByte
        ("throttle",    DataTypes.UNSIGNED_INT8.value), # Throttle (RANGE: 0 -> 255)
        ("brake",       DataTypes.UNSIGNED_INT8.value), # Brake (RANGE: 0 -> 255)
        ("PADDING",     DataTypes.UNSIGNED_INT8.value), # Padding byte # * might not be needed
        
        ("roadPlane",               DataTypes.FLOAT.value * 3),     # Banking of the road
        ("roadPlaneDistance",       DataTypes.FLOAT.value),         # Distance above or below the plane, e.g a dip in the road is negative, hill is positive.
        ("wheelRPS",                DataTypes.FLOAT.value * 4),     # Revolutions per second of tyres in rads
        ("tyreRadius",              DataTypes.FLOAT.value * 4),     # Radius of the tyre in meters
        ("suspHeight",              DataTypes.FLOAT.value * 4),     # Suspension height of the car
        ("UNKNOWNFLOATS",           DataTypes.FLOAT.value * 8),     # Unknown float (from original source)
        ("clutch",                  DataTypes.FLOAT.value),         # Clutch (RANGE: 0.0 -> 1.0)
        ("clutchEngagement",        DataTypes.FLOAT.value),         # Clutch Engangement (RANGE: 0.0 -> 1.0)
        ("RPMFromClutchToGearbox",  DataTypes.FLOAT.value),         # Pretty much same as engine RPM, is 0 when clutch is depressed
        ("transmissionTopSpeed",    DataTypes.FLOAT.value),         # Top speed as gear ratio value
        ("gearRatios",              DataTypes.FLOAT.value  * 8),    # Gear ratios of the car up to 8
        ("carCode",                 DataTypes.SIGNED_INT32.value),  # This value may be overriden if using a car with more then 9 gears
        
        ("wheelRotation",   DataTypes.FLOAT.value),  # Calculates the wheel rotation in radians
        ("UNKNOWNFLOAT10",  DataTypes.FLOAT.value),  # Unknown float
        ("sway",            DataTypes.FLOAT.value),  # X axis acceleration
        ("heave",           DataTypes.FLOAT.value),  # Y axis acceleration
        ("surge",           DataTypes.FLOAT.value),  # Z axis acceleration
        
        ("throttleFiltered",    DataTypes.UNSIGNED_INT8.value),     # Filtered Throttle Output
        ("brakeFiltered",       DataTypes.UNSIGNED_INT8.value),     # Filtered Brake Output
        ("UNKNOWNUINT81",       DataTypes.UNSIGNED_INT8.value),     # Unknown unsigned 8 bit integer
        ("UNKNOWNUINT82",       DataTypes.UNSIGNED_INT8.value),     # Unknown unsigned 8 bit integer
        ("torqueVectors",       DataTypes.FLOAT.value * 4),         # Torque vectoring for certain cars - Positive = driving force - Negative = braking or regenerating
        ("energyRecovery",      DataTypes.FLOAT.value),             # Energy being recovered to the battery
        ("UNKNOWNFLOAT11",      DataTypes.FLOAT.value),             # Unknown float
    ]


class PacketCData(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("magic",                       DataTypes.SIGNED_INT32.value),  # Magic, different value defines what game is being played
        ("position",                    DataTypes.FLOAT.value * 3),     # Position on Track in meters in each axis
        ("worldVelocity",               DataTypes.FLOAT.value * 3),     # Velocity in meters for each axis
        ("rotation",                    DataTypes.FLOAT.value * 3),     # Rotation (Pitch/Yaw/Roll) (RANGE: -1 -> 1)
        ("orientationRelativeToNorth",  DataTypes.FLOAT.value),         # Orientation to North (RANGE: 1.0 (North) -> 0.0 (South))
        ("angularVelocity",             DataTypes.FLOAT.value * 3),     # Speed at which the car turns around axis in rad/s (RANGE: -1 -> 1)
        ("bodyHeight",                  DataTypes.FLOAT.value),         # Body height
        ("EngineRPM",                   DataTypes.FLOAT.value),         # Engine revolutions per minute

        ("iv",              DataTypes.UNSIGNED_INT8.value * 4),     # IV for Salsa20 encryption/decryption
        ("fuelLevel",       DataTypes.FLOAT.value),                 # Fuel level of car in liters 
        ("fuelCapacity",    DataTypes.FLOAT.value),                 # Max fuel capacity for current car (RANGE: 100 (most cars) -> 5 (karts) -> 0 (electric cars))  
        ("speed",           DataTypes.FLOAT.value),                 # Speed in m/s
        ("boost",           DataTypes.FLOAT.value),                 # Offset by +1 (EXAMPLE: 1.0 = 0 X 100kPa, 2.0 = 1 x 100kPa) # TODO apply -1 offset (from original source)
        ("oilPressure",     DataTypes.FLOAT.value),                 # Oil pressure in bars
        ("waterTemp",       DataTypes.FLOAT.value),                 # Constantly 85
        ("oilTemp",         DataTypes.FLOAT.value),                 # Constantly 110
        ("tyreTemp",        DataTypes.FLOAT.value * 4),             # Tyre temp for all 4 tires (FL -> FR -> RL -> RR)
        
        ("packetId",            DataTypes.SIGNED_INT32.value),  # ID of packet
        ("lapCount",            DataTypes.SIGNED_INT16.value),  # Lap count
        ("totalLaps",           DataTypes.SIGNED_INT16.value),  # Laps to finish
        ("bestLaptime",         DataTypes.SIGNED_INT32.value),  # Best lap time, defaults to -1 if not set
        ("lastLaptime",         DataTypes.SIGNED_INT32.value),  # Previous lap time, defaults to -1 if not set
        ("dayProgression",      DataTypes.SIGNED_INT32.value),  # Current time of day on track in ms
        ("RaceStartPosition",   DataTypes.SIGNED_INT16.value),  # Position of the car before the start of the race, defaults to -1 after race start
        ("preRaceNumCars",      DataTypes.SIGNED_INT16.value),  # Number of cars before the race start, defaults to -1 after start of the race
        ("minAlertRPM",         DataTypes.SIGNED_INT16.value),  # Minimum RPM that the rev limiter displays an alert
        ("maxAlertRPM",         DataTypes.SIGNED_INT16.value),  # Maximum RPM that the rev limiter displays an alert
        ("calcMaxSpeed",        DataTypes.SIGNED_INT16.value),  # Highest possible speed achievable of the current transmission settings
        
        ("flags",           DataTypes.SIGNED_INT16.value), # Packet flags # TODO: Get working (from original source)
        
        ("gears",       DataTypes.UNSIGNED_INT8.value), # First 4 bits: Current Gear, Last 4 bits: Suggested Gear, # TODO see getCurrentGearFromByte and getSuggestedGearFromByte
        ("throttle",    DataTypes.UNSIGNED_INT8.value), # Throttle (RANGE: 0 -> 255)
        ("brake",       DataTypes.UNSIGNED_INT8.value), # Brake (RANGE: 0 -> 255)
        ("PADDING",     DataTypes.UNSIGNED_INT8.value), # Padding byte # * might not be needed
        
        ("roadPlane",               DataTypes.FLOAT.value * 3),     # Banking of the road
        ("roadPlaneDistance",       DataTypes.FLOAT.value),         # Distance above or below the plane, e.g a dip in the road is negative, hill is positive.
        ("wheelRPS",                DataTypes.FLOAT.value * 4),     # Revolutions per second of tyres in rads
        ("tyreRadius",              DataTypes.FLOAT.value * 4),     # Radius of the tyre in meters
        ("suspHeight",              DataTypes.FLOAT.value * 4),     # Suspension height of the car
        ("UNKNOWNFLOATS",           DataTypes.FLOAT.value * 8),     # Unknown float (from original source)
        ("clutch",                  DataTypes.FLOAT.value),         # Clutch (RANGE: 0.0 -> 1.0)
        ("clutchEngagement",        DataTypes.FLOAT.value),         # Clutch Engangement (RANGE: 0.0 -> 1.0)
        ("RPMFromClutchToGearbox",  DataTypes.FLOAT.value),         # Pretty much same as engine RPM, is 0 when clutch is depressed
        ("transmissionTopSpeed",    DataTypes.FLOAT.value),         # Top speed as gear ratio value
        ("gearRatios",              DataTypes.FLOAT.value  * 8),    # Gear ratios of the car up to 8
        ("carCode",                 DataTypes.SIGNED_INT32.value),  # This value may be overriden if using a car with more then 9 gears
        
        ("wheelRotation",   DataTypes.FLOAT.value),  # Calculates the wheel rotation in radians
        ("UNKNOWNFLOAT10",  DataTypes.FLOAT.value),  # Unknown float
        ("sway",            DataTypes.FLOAT.value),  # X axis acceleration
        ("heave",           DataTypes.FLOAT.value),  # Y axis acceleration
        ("surge",           DataTypes.FLOAT.value),  # Z axis acceleration
        
        ("throttleFiltered",    DataTypes.UNSIGNED_INT8.value),     # Filtered Throttle Output
        ("brakeFiltered",       DataTypes.UNSIGNED_INT8.value),     # Filtered Brake Output
        ("UNKNOWNUINT81",       DataTypes.UNSIGNED_INT8.value),     # Unknown unsigned 8 bit integer
        ("UNKNOWNUINT82",       DataTypes.UNSIGNED_INT8.value),     # Unknown unsigned 8 bit integer
        ("torqueVectors",       DataTypes.FLOAT.value * 4),         # Torque vectoring for certain cars - Positive = driving force - Negative = braking or regenerating
        ("energyRecovery",      DataTypes.FLOAT.value),             # Energy being recovered to the battery
        ("UNKNOWNFLOAT11",      DataTypes.FLOAT.value),             # Unknown float
        
        ("surfaceType",     DataTypes.CHAR.value * 4),          # The kind of surface in contact with the tyres (T: tarmac, C: curb/kerb D: Dirt/Grass)
        ("currentLap",      DataTypes.SIGNED_INT32.value),      # The current lap being set in milliseconds
        ("UNKNOWNFLOATS",   DataTypes.FLOAT.value * 3),         # Unknown float
        ("carCategory",     DataTypes.CHAR.value * 4),          # Null terminated string of car category (GR3, GRX etc.)
    ]



### Heart Beat

def heartBeat(socket, destination: tuple[int, int], msg = b'C'):
    
    socket.sendto(msg, destination)
    
    # send message to destination
    # msg = packetVersion = A | B | ~
    # else packetVersion = A 

### Decryption

# pip install pycryptodome
try:
    from Crypto.Cipher import Salsa20 as s20
except:
    print("Cant use GT7 struct! Install pycryptodome. 'pip install pycryptodome'")
import struct
def decrypt_data(raw: bytes) -> bytes:
    def detect_packet_version(data: bytes) -> str:
        size = len(data)
        return {296: 'A', 316: 'B', 344: '~', 368: 'C'}.get(size, ' ')
    
    SALSA20_KEY = b"Simulator Interface Packet GT7 ver 0.0"[:32]

    XOR_MAP = {
        'A': 0xDEADBEAF,
        'B': 0xDEADBEEF,
        '~': 0x55FABB4F,
        'C': 0xDEADBEEF,
    }
    
    version = detect_packet_version(raw)

    # Read iv1 as a little-endian uint32 from offset 0x40
    iv1int = struct.unpack_from("<I", raw, 0x40)[0]

    xor_val = XOR_MAP.get(version, 0)
    iv2int = iv1int ^ xor_val

    # IV is [iv2 as LE bytes] + [iv1 as LE bytes]  — matches C++ layout
    iv = struct.pack("<I", iv2int) + struct.pack("<I", iv1int)

    cipher = s20.new(key=SALSA20_KEY, nonce=iv)
    decrypted = cipher.decrypt(raw)
    return decrypted

### MetaData

class MetaData:
    port: int = 33740
    fullBufferSize: int = 368
    
    destinationPort = 33739
    heartBeatFunc = heartBeat
    decrytionFunc = decrypt_data
    
    headerInfo: tuple[int, type | None] = (0, None)
    packetIDAttribute: str | None = None
    
    packetInfo: dict[int, tuple[tuple[int, type], ...]] = {
        0: ((296, PacketAData), (316, PacketBData), (344, PacketTildaData), (368, PacketCData)),
    }