import ctypes
from enum import Enum


class DataTypes(Enum):
    STRUCTURE = ctypes.LittleEndianStructure
    UNION = ctypes.Union
    
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT16 = ctypes.c_int16
    # SIGNED_INT32 = ctypes.c_int32
    
    UNSIGNED_INT8 = ctypes.c_uint8      # 1 byte 
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT32 = ctypes.c_uint32
    UNSIGNED_INT64 = ctypes.c_uint64
    
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    DOUBLE = ctypes.c_double
    
    BYTE = ctypes.c_byte


### Motion Packet -- Rate as specified in menus -- 1341 bytes


class CarUDPData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_worldPosition",         DataTypes.FLOAT.value * 3),     # world co-ordinates of vehicle
        ("m_lastLapTime",           DataTypes.FLOAT.value),
        ("m_currentLapTime",        DataTypes.FLOAT.value),
        ("m_bestLapTime",           DataTypes.FLOAT.value),
        ("m_sector1Time",           DataTypes.FLOAT.value),
        ("m_sector2Time",           DataTypes.FLOAT.value),
        ("m_lapDistance",           DataTypes.FLOAT.value),
        ("m_driverId",              DataTypes.BYTE.value),
        ("m_teamId",                DataTypes.BYTE.value),
        ("m_carPosition",           DataTypes.BYTE.value),          # track positions of vehicle
        ("m_currentLapNum",         DataTypes.BYTE.value),
        ("m_tyreCompound",          DataTypes.BYTE.value),          # compound of tyre – 0 = ultra soft, 1 = super soft, 2 = soft, 3 = medium, 4 = hard, 5 = inter, 6 = wet
        ("m_inPits",                DataTypes.BYTE.value),          # 0 = none, 1 = pitting, 2 = in pit area
        ("m_sector",                DataTypes.BYTE.value),          # 0 = sector1, 1 = sector2, 2 = sector3
        ("m_currentLapInvalid",     DataTypes.BYTE.value),          # current lap invalid - 0 = valid, 1 = invalid
        ("m_penalties",             DataTypes.BYTE.value),          # accumulated time penalties in seconds to be added
    ]


class UDPPacket(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_time",                      DataTypes.FLOAT.value),
        ("m_lapTime",                   DataTypes.FLOAT.value),
        ("m_lapDistance",               DataTypes.FLOAT.value),
        ("m_totalDistance",             DataTypes.FLOAT.value),
        ("m_x",                         DataTypes.FLOAT.value),         # World space position
        ("m_y",                         DataTypes.FLOAT.value),         # World space position
        ("m_z",                         DataTypes.FLOAT.value),         # World space position
        ("m_speed",                     DataTypes.FLOAT.value),         # Speed of car in MPH
        ("m_xv",                        DataTypes.FLOAT.value),         # Velocity in world space
        ("m_yv",                        DataTypes.FLOAT.value),         # Velocity in world space
        ("m_zv",                        DataTypes.FLOAT.value),         # Velocity in world space
        ("m_xr",                        DataTypes.FLOAT.value),         # World space right direction
        ("m_yr",                        DataTypes.FLOAT.value),         # World space right direction
        ("m_zr",                        DataTypes.FLOAT.value),         # World space right direction
        ("m_xd",                        DataTypes.FLOAT.value),         # World space forward direction
        ("m_yd",                        DataTypes.FLOAT.value),         # World space forward direction
        ("m_zd",                        DataTypes.FLOAT.value),         # World space forward direction
        ("m_susp_pos",                  DataTypes.FLOAT.value * 4),     # Note: All wheel arrays have the order:
        ("m_susp_vel",                  DataTypes.FLOAT.value * 4),     # RL, RR, FL, FR
        ("m_wheel_speed",               DataTypes.FLOAT.value * 4),
        ("m_throttle",                  DataTypes.FLOAT.value),
        ("m_steer",                     DataTypes.FLOAT.value),
        ("m_brake",                     DataTypes.FLOAT.value),
        ("m_clutch",                    DataTypes.FLOAT.value),
        ("m_gear",                      DataTypes.FLOAT.value),
        ("m_gforce_lat",                DataTypes.FLOAT.value),
        ("m_gforce_lon",                DataTypes.FLOAT.value),
        ("m_lap",                       DataTypes.FLOAT.value),
        ("m_engineRate",                DataTypes.FLOAT.value),
        ("m_sli_pro_native_support",    DataTypes.FLOAT.value),     # SLI Pro support
        ("m_car_position",              DataTypes.FLOAT.value),     # car race position
        ("m_kers_level",                DataTypes.FLOAT.value),     # kers energy left
        ("m_kers_max_level",            DataTypes.FLOAT.value),     # kers maximum energy
        ("m_drs",                       DataTypes.FLOAT.value),     # 0 = off, 1 = on
        ("m_traction_control",          DataTypes.FLOAT.value),     # 0 (off) - 2 (high)
        ("m_anti_lock_brakes",          DataTypes.FLOAT.value),     # 0 (off) - 1 (on)
        ("m_fuel_in_tank",              DataTypes.FLOAT.value),     # current fuel mass
        ("m_fuel_capacity",             DataTypes.FLOAT.value),     # fuel capacity
        ("m_in_pits",                   DataTypes.FLOAT.value),     # 0 = none, 1 = pitting, 2 = in pit area
        ("m_sector",                    DataTypes.FLOAT.value),     # 0 = sector1, 1 = sector2, 2 = sector3
        ("m_sector1_time",              DataTypes.FLOAT.value),     # time of sector1 (or 0)
        ("m_sector2_time",              DataTypes.FLOAT.value),     # time of sector2 (or 0)
        ("m_brakes_temp",               DataTypes.FLOAT.value),     # brakes temperature (centigrade)
        ("m_tyres_pressure",            DataTypes.FLOAT.value),     # tyres pressure PSI
        ("m_team_info",                 DataTypes.FLOAT.value),     # team ID 
        ("m_total_laps",                DataTypes.FLOAT.value),     # total number of laps in this race
        ("m_track_size",                DataTypes.FLOAT.value),     # track size meters
        ("m_last_lap_time",             DataTypes.FLOAT.value),     # last lap time
        ("m_max_rpm",                   DataTypes.FLOAT.value),     # cars max RPM, at which point the rev limiter will kick in
        ("m_idle_rpm",                  DataTypes.FLOAT.value),     # cars idle RPM
        ("m_max_gears",                 DataTypes.FLOAT.value),     # maximum number of gears
        ("m_sessionType",               DataTypes.FLOAT.value),     # 0 = unknown, 1 = practice, 2 = qualifying, 3 = race
        ("m_drsAllowed",                DataTypes.FLOAT.value),     # 0 = not allowed, 1 = allowed, -1 = invalid / unknown
        ("m_track_number",              DataTypes.FLOAT.value),     # -1 for unknown, 0-21 for tracks
        ("m_vehicleFIAFlags",           DataTypes.FLOAT.value),     # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
        ("m_era",                       DataTypes.FLOAT.value),     # era, 2017 (modern) or 1980 (classic)
        ("m_engine_temperature",        DataTypes.FLOAT.value),     # engine temperature (centigrade)
        ("m_gforce_vert",               DataTypes.FLOAT.value),     # vertical g-force component
        ("m_ang_vel_x",                 DataTypes.FLOAT.value),     # angular velocity x-component
        ("m_ang_vel_y",                 DataTypes.FLOAT.value),     # angular velocity y-component
        ("m_ang_vel_z",                 DataTypes.FLOAT.value),     # angular velocity z-component
        ("m_tyres_temperature",         DataTypes.BYTE.value),      # tyres temperature (centigrade)
        ("m_tyres_wear",                DataTypes.BYTE.value),      # tyre wear percentage
        ("m_tyre_compound",             DataTypes.BYTE.value),      # compound of tyre – 0 = ultra soft, 1 = super soft, 2 = soft, 3 = medium, 4 = hard, 5 = inter, 6 = wet
        ("m_front_brake_bias",          DataTypes.BYTE.value),      # front brake bias (percentage)
        ("m_fuel_mix",                  DataTypes.BYTE.value),      # fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
        ("m_currentLapInvalid",         DataTypes.BYTE.value),      # current lap invalid - 0 = valid, 1 = invalid
        ("m_tyres_damage",              DataTypes.BYTE.value),      # tyre damage (percentage)
        ("m_front_left_wing_damage",    DataTypes.BYTE.value),      # front left wing damage (percentage)
        ("m_front_right_wing_damage",   DataTypes.BYTE.value),      # front right wing damage (percentage)
        ("m_rear_wing_damage",          DataTypes.BYTE.value),      # rear wing damage (percentage)
        ("m_engine_damage",             DataTypes.BYTE.value),      # engine damage (percentage)
        ("m_gear_box_damage",           DataTypes.BYTE.value),      # gear box damage (percentage)
        ("m_exhaust_damage",            DataTypes.BYTE.value),      # exhaust damage (percentage)
        ("m_pit_limiter_status",        DataTypes.BYTE.value),      # pit limiter status – 0 = off, 1 = on
        ("m_pit_speed_limit",           DataTypes.BYTE.value),      # pit speed limit in mph
        ("m_session_time_left",         DataTypes.FLOAT.value),     # time left in session in seconds 
        ("m_rev_lights_percent",        DataTypes.BYTE.value),      # rev lights indicator (percentage)
        ("m_is_spectating",             DataTypes.BYTE.value),      # whether the player is spectating
        ("m_spectator_car_index",       DataTypes.BYTE.value),      # index of the car being spectated
        # Car data
        ("m_num_cars",              DataTypes.BYTE.value),      # number of cars in data
        ("m_player_car_index",      DataTypes.BYTE.value),      # index of player's car in the array
        ("m_car_data",              CarUDPData * 20),           # data for all cars on track
        ("m_yaw",                   DataTypes.FLOAT.value),
        ("m_pitch",                 DataTypes.FLOAT.value),
        ("m_roll",                  DataTypes.FLOAT.value),
        ("m_x_local_velocity",      DataTypes.FLOAT.value),     # Velocity in local space
        ("m_y_local_velocity",      DataTypes.FLOAT.value),     # Velocity in local space
        ("m_z_local_velocity",      DataTypes.FLOAT.value),     # Velocity in local space
        ("m_susp_acceleration",     DataTypes.FLOAT.value),     # RL, RR, FL, FR
        ("m_ang_acc_x",             DataTypes.FLOAT.value),     # angular acceleration x-component
        ("m_ang_acc_y",             DataTypes.FLOAT.value),     # angular acceleration x-component
        ("m_ang_acc_z",             DataTypes.FLOAT.value),     # angular acceleration x-component
    ]



### MetaData

class MetaData:
    # standard network info
    port: int = 20777
    fullBufferSize: int = 1289
    
    # use if a heartbeat is needed
    heartBeatPort = None
    heartBeatFunc = None
    
    # use for itinial hand shake
    handShakePort = None
    handShakeFunc = None
    
    # use if the data needs decrypting
    decrytionFunc = None
    
    # use if there is a header packet
    headerInfo: tuple[int, type | None] = (0, None)
    packetIDAttribute: str | None = None
    
    # standard packet info
    packetInfo: dict[int, tuple[tuple[int, type], ...]] = {
        0: ((1289, UDPPacket),),
    }

