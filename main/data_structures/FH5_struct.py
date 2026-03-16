import ctypes
from enum import Enum

# source
# https://forums.forza.net/t/data-out-telemetry-variables-and-structure/535984/2
# https://pastebin.com/GFbbzbg3

class DataTypes(Enum):
    STRUCTURE = ctypes.LittleEndianStructure
    
    SIGNED_INT = ctypes.c_int
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT32 = ctypes.c_int32
    
    UNSIGNED_INT = ctypes.c_uint
    UNSIGNED_INT8 = ctypes.c_uint8
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT32 = ctypes.c_uint32
    
    FLOAT = ctypes.c_float


class DashData(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("IsRaceOn",            DataTypes.SIGNED_INT32.value),  # 1 when race is on. = 0 when in menus/race stopped
        # Can overflow to 0 eventually      
        ("TimestampMS",         DataTypes.UNSIGNED_INT32.value),          
        ("EngineMaxRpm",        DataTypes.FLOAT.value),
        ("EngineIdleRpm",       DataTypes.FLOAT.value),
        ("CurrentEngineRpm",    DataTypes.FLOAT.value),
        # In the car's local space; X = right, Y = up, Z = forward
        ("AccelerationX",       DataTypes.FLOAT.value),
        ("AccelerationY",       DataTypes.FLOAT.value),
        ("AccelerationZ",       DataTypes.FLOAT.value),
        # In the car's local space; X = right, Y = up, Z = forward
        ("VelocityX",           DataTypes.FLOAT.value),
        ("VelocityY",           DataTypes.FLOAT.value),
        ("VelocityZ",           DataTypes.FLOAT.value),
        # In the car's local space; X = pitch, Y = yaw, Z = roll
        ("AngularVelocityX",    DataTypes.FLOAT.value),
        ("AngularVelocityY",    DataTypes.FLOAT.value),
        ("AngularVelocityZ",    DataTypes.FLOAT.value),
        
        ("Yaw",                 DataTypes.FLOAT.value),
        ("Pitch",               DataTypes.FLOAT.value),
        ("Roll",                DataTypes.FLOAT.value),
        # Suspension travel normalized: 0.0f = max stretch; 1.0 = max compression
        ("NormalizedSuspensionTravelFrontLeft",     DataTypes.FLOAT.value),
        ("NormalizedSuspensionTravelFrontRight",    DataTypes.FLOAT.value),
        ("NormalizedSuspensionTravelRearLeft",      DataTypes.FLOAT.value),
        ("NormalizedSuspensionTravelRearRight",     DataTypes.FLOAT.value),
        # Tire normalized slip ratio, = 0 means 100% grip and |ratio| > 1.0 means loss of grip.
        ("TireSlipRatioFrontLeft",          DataTypes.FLOAT.value),
        ("TireSlipRatioFrontRight",         DataTypes.FLOAT.value),
        ("TireSlipRatioRearLeft",           DataTypes.FLOAT.value),
        ("TireSlipRatioRearRight",          DataTypes.FLOAT.value),
        # Wheels rotation speed radians/sec. 
        ("WheelRotationSpeedFrontLeft",     DataTypes.FLOAT.value),
        ("WheelRotationSpeedFrontRight",    DataTypes.FLOAT.value),
        ("WheelRotationSpeedRearLeft",      DataTypes.FLOAT.value),
        ("WheelRotationSpeedRearRight",     DataTypes.FLOAT.value),
        # 1 when wheel is on rumble strip, = 0 when off.
        ("WheelOnRumbleStripFrontLeft",     DataTypes.SIGNED_INT32.value),
        ("WheelOnRumbleStripFrontRight",    DataTypes.SIGNED_INT32.value),
        ("WheelOnRumbleStripRearLeft",      DataTypes.SIGNED_INT32.value),
        ("WheelOnRumbleStripRearRight",     DataTypes.SIGNED_INT32.value),
        # from 0 to 1, where 1 is the deepest puddle
        ("WheelInPuddleDepthFrontLeft",     DataTypes.FLOAT.value),
        ("WheelInPuddleDepthFrontRight",    DataTypes.FLOAT.value),
        ("WheelInPuddleDepthRearLeft",      DataTypes.FLOAT.value),
        ("WheelInPuddleDepthRearRight",     DataTypes.FLOAT.value),
        # Non-dimensional surface rumble values passed to controller force feedback
        ("SurfaceRumbleFrontLeft",          DataTypes.FLOAT.value),
        ("SurfaceRumbleFrontRight",         DataTypes.FLOAT.value),
        ("SurfaceRumbleRearLeft",           DataTypes.FLOAT.value),
        ("SurfaceRumbleRearRight",          DataTypes.FLOAT.value),
        # Tire normalized slip angle, = 0 means 100% grip and |angle| > 1.0 means loss of grip.
        ("TireSlipAngleFrontLeft",          DataTypes.FLOAT.value),
        ("TireSlipAngleFrontRight",         DataTypes.FLOAT.value),
        ("TireSlipAngleRearLeft",           DataTypes.FLOAT.value),
        ("TireSlipAngleRearRight",          DataTypes.FLOAT.value),
        # Tire normalized combined slip, = 0 means 100% grip and |slip| > 1.0 means loss of grip.
        ("TireCombinedSlipFrontLeft",       DataTypes.FLOAT.value),
        ("TireCombinedSlipFrontRight",      DataTypes.FLOAT.value),
        ("TireCombinedSlipRearLeft",        DataTypes.FLOAT.value),
        ("TireCombinedSlipRearRight",       DataTypes.FLOAT.value),
        # Actual suspension travel in meters
        ("SuspensionTravelMetersFrontLeft",     DataTypes.FLOAT.value),
        ("SuspensionTravelMetersFrontRight",    DataTypes.FLOAT.value),
        ("SuspensionTravelMetersRearLeft",      DataTypes.FLOAT.value),
        ("SuspensionTravelMetersRearRight",     DataTypes.FLOAT.value),
        
        ("CarOrdinal",              DataTypes.SIGNED_INT32.value),  # Unique ID of the car make/model
        ("CarClass",                DataTypes.SIGNED_INT32.value),  # Between 0 (D -- worst cars) and 7 (X class -- best cars) inclusive      
        ("CarPerformanceIndex",     DataTypes.SIGNED_INT32.value),  # Between 100 (worst car) and 999 (best car) inclusive
        ("DrivetrainType",          DataTypes.SIGNED_INT32.value),  # 0 = FWD, 1 = RWD, 2 = AWD
        ("NumCylinders",            DataTypes.SIGNED_INT32.value),  # Number of cylinders in the engine
        
        ("CarCategory",     DataTypes.SIGNED_INT32.value),
        ("Unknown1",        DataTypes.SIGNED_INT32.value),
        ("Unknown2",        DataTypes.SIGNED_INT32.value),
        
        # Dash data
        ("PositionX",           DataTypes.FLOAT.value),
        ("PositionY",           DataTypes.FLOAT.value),
        ("PositionZ",           DataTypes.FLOAT.value),
        ("Speed",               DataTypes.FLOAT.value),
        ("Power",               DataTypes.FLOAT.value),
        ("Torque",              DataTypes.FLOAT.value),
        ("TireTempFrontLeft",   DataTypes.FLOAT.value),
        ("TireTempFrontRight",  DataTypes.FLOAT.value),
        ("TireTempRearLeft",    DataTypes.FLOAT.value),
        ("TireTempRearRight",   DataTypes.FLOAT.value),
        ("Boost",               DataTypes.FLOAT.value),
        ("Fuel",                DataTypes.FLOAT.value),
        ("DistanceTraveled",    DataTypes.FLOAT.value),
        ("BestLap",             DataTypes.FLOAT.value),
        ("LastLap",             DataTypes.FLOAT.value),
        ("CurrentLap",          DataTypes.FLOAT.value),
        ("CurrentRaceTime",     DataTypes.FLOAT.value),
        
        ("LapNumber",       DataTypes.UNSIGNED_INT16.value),
        ("RacePosition",    DataTypes.UNSIGNED_INT8.value),
        ("Accel",           DataTypes.UNSIGNED_INT8.value),
        ("Brake",           DataTypes.UNSIGNED_INT8.value),
        ("Clutch",          DataTypes.UNSIGNED_INT8.value),
        ("HandBrake",       DataTypes.UNSIGNED_INT8.value),
        ("Gear",            DataTypes.UNSIGNED_INT8.value),
        ("Steer",           DataTypes.SIGNED_INT8.value),
        ("NormalizedDrivingLine",           DataTypes.SIGNED_INT8.value),
        ("NormalizedAIBrakeDifference",     DataTypes.SIGNED_INT8.value),
    ]

### MetaData

class MetaData:
    port: int = 5300
    fullBufferSize: int = 324
    headerInfo: tuple[int, type | None] = (0, None)
    packetIDAttribute: str | None = None
    packetInfo: dict[int, tuple[tuple[int, type], ...]] = {
        0: ((324, DashData),),
    }