import ctypes
from enum import Enum

# source
# https://docs.google.com/document/d/1KfkZiIluXZ6mMhLWfDX1qAGbvhGRC3ZUzjVIt5FQpp4/pub

class DataTypes(Enum):
    STRUCTURE = ctypes.LittleEndianStructure
    
    SIGNED_INT = ctypes.c_int
    
    BOOL = ctypes.c_bool
    FLOAT = ctypes.c_float
    # CHAR = ctypes.c_char
    CHAR = ctypes.c_wchar

# If the client subscribed himself with SUBSCRIBE_UPDATE identifier, it will receive the following structured data
class RTCarData(DataTypes.STRUCTURE.value):
    # _pack_ = 1 # ! Do Not Enable or data will be wrong
    _fields_ = [
        ("identifier",  DataTypes.CHAR.value),          # is set to char “a” , it is used to understand that the structured data is the data that the client app wants
        ("size",        DataTypes.SIGNED_INT.value),    # the size of the structured data in Bytes
        
        ("speed_Kmh",   DataTypes.FLOAT.value),
        ("speed_Mph",   DataTypes.FLOAT.value),
        ("speed_Ms",    DataTypes.FLOAT.value),
        
        ("isAbsEnabled",        DataTypes.BOOL.value),
        ("isAbsInAction",       DataTypes.BOOL.value),
        ("isTcInAction",        DataTypes.BOOL.value),
        ("isTcEnabled",         DataTypes.BOOL.value),
        ("isInPit",             DataTypes.BOOL.value),
        ("isEngineLimiterOn",   DataTypes.BOOL.value),
        
        # ("Unknown1", ctypes.c_bool),
        # ("Unknown2", ctypes.c_bool),
        # might be 2 unknown bytes
        
        ("accG_vertical",       DataTypes.FLOAT.value),
        ("accG_horizontal",     DataTypes.FLOAT.value),
        ("accG_frontal",        DataTypes.FLOAT.value),
        
        ("lapTime",     DataTypes.SIGNED_INT.value),
        ("lastLap",     DataTypes.SIGNED_INT.value),
        ("bestLap",     DataTypes.SIGNED_INT.value),
        ("lapCount",    DataTypes.SIGNED_INT.value),
        
        ("gas",         DataTypes.FLOAT.value),
        ("brake",       DataTypes.FLOAT.value),
        ("clutch",      DataTypes.FLOAT.value),
        ("engineRPM",   DataTypes.FLOAT.value),
        ("steer",       DataTypes.FLOAT.value),
        ("gear",        DataTypes.SIGNED_INT.value),
        ("cgHeight",    DataTypes.FLOAT.value),
        
        ("wheelAngularSpeed",           DataTypes.FLOAT.value * 4),
        ("slipAngle",                   DataTypes.FLOAT.value * 4),
        ("slipAngle_ContactPatch",      DataTypes.FLOAT.value * 4),
        ("slipRatio",                   DataTypes.FLOAT.value * 4),
        ("tyreSlip",                    DataTypes.FLOAT.value * 4),
        ("ndSlip",                      DataTypes.FLOAT.value * 4),
        ("load",                        DataTypes.FLOAT.value * 4),
        ("Dy",                          DataTypes.FLOAT.value * 4),
        ("Mz",                          DataTypes.FLOAT.value * 4),
        ("tyreDirtyLevel",              DataTypes.FLOAT.value * 4),
        
        ("camberRAD",           DataTypes.FLOAT.value * 4),
        ("tyreRadius",          DataTypes.FLOAT.value * 4),
        ("tyreLoadedRadius",    DataTypes.FLOAT.value * 4),
        
        ("suspensionHeight",        DataTypes.FLOAT.value * 4),
        ("carPositionNormalized",   DataTypes.FLOAT.value),
        ("carSlope",                DataTypes.FLOAT.value),
        ("carCoordinates",          DataTypes.FLOAT.value * 3),

    ]

# If the client subscribed himself with SUBSCRIBE_SPOT identifier, it will receive the following structured data whenever a spot event is triggered (for example for the end of a lap). 
# Differently from SUBSCRIBE_UPDATE, this event will interest all the cars in the AC session
class RTLapData(DataTypes.STRUCTURE.value):
    _pack_ = 1
    _fields_ = [
        ("carIdentifierNumber",     DataTypes.SIGNED_INT.value),
        ("lap",                     DataTypes.SIGNED_INT.value),
        ("driverName",              DataTypes.CHAR.value * 50),
        ("carName",                 DataTypes.CHAR.value * 50),
        ("time",                    DataTypes.SIGNED_INT.value),
    ]


### Hand Shake

# The PC running Assetto Corsa will be referred as the ACServer.

# [not used in the current Remote Telemtry version by AC] In future versions it will identify the platform type of the client. This will be used to adjust a specific behaviour for each platform
# [not used in the current Remote Telemtry version by AC] In future version this field will identify the AC Remote Telemetry version that the device expects to speak with.
# This is the type of operation required by the client. The following operations are now available:
#   HANDSHAKE = 0 :         This operation identifier must be set when the client wants to start the comunication.
#   SUBSCRIBE_UPDATE = 1 :  This operation identifier must be set when the client wants to be updated from the specific ACServer.
#   SUBSCRIBE_SPOT = 2 :    This operation identifier must be set when the client wants to be updated from the specific ACServer just for SPOT Events (e.g.: the end of a lap).
#   DISMISS = 3 :           This operation identifier must be set when the client wants to leave the comunication with ACServer.

class handshaker(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("identifier",      DataTypes.SIGNED_INT.value),
        ("version",         DataTypes.SIGNED_INT.value),
        ("operationId",     DataTypes.SIGNED_INT.value),
    ]
    def __init__(self, operationID, identifier=1, version=1):
        super().__init__(identifier=identifier, version=version, operationId=operationID)

class handshackerResponse(DataTypes.STRUCTURE.value): # might be 408 or 308
    _pack_ = 1
    _fields_ = [
        ("carName",         DataTypes.CHAR.value * 50),     # is the name of the car that the player is driving on the AC Server
        ("driverName",      DataTypes.CHAR.value * 50),     # is the name of the driver running on the AC Server
        ("identifier",      DataTypes.SIGNED_INT.value),    # for now is just 4242, this code will identify different status, as “NOT AVAILABLE” for connection
        ("version",         DataTypes.SIGNED_INT.value),    # for now is set to 1, this will identify the version running on the AC Server
        ("trackName",       DataTypes.CHAR.value * 50),     # is the name of the track on the AC Server
        ("trackConfig",     DataTypes.CHAR.value * 50),     # is the track configuration
    ]

def startHandShake(socket, destination: tuple[int, int]):
    handShakeMSG = handshaker(operationID = 0)
    prepHandShake = bytes(handShakeMSG)
    
    socket.sendto(prepHandShake, destination)
        
    handShakeMSG = handshaker(operationID = 1)
    prepHandShake = bytes(handShakeMSG)
    socket.sendto(prepHandShake, destination)
    
    handShakeMSG = handshaker(operationID = 2)
    prepHandShake = bytes(handShakeMSG)
    socket.sendto(prepHandShake, destination)

def endHandShake(socket, destination: tuple[int, int]):
    handShakeMSG = handshaker(operationID = 3)
    prepHandShake = bytes(handShakeMSG)
    
    socket.sendto(prepHandShake, destination)


### Decryption


### MetaData

class MetaData:
    # standard network info
    port: int = 9997
    fullBufferSize: int = 1500
    
    # use if a heartbeat is needed
    heartBeatPort = None
    heartBeatFunc = None
    
    # use for itinial hand shake
    handShakePort = 9996
    handShakeFunc = (startHandShake, endHandShake)
    
    # use if the data needs decrypting
    decrytionFunc = None
    
    # use if there is a header packet
    headerInfo: tuple[int, type | None] = (0, None)
    packetIDAttribute: str | None = None
    
    # standard packet info
    packetInfo: dict[int, tuple[tuple[int, type], ...]] = {
        0: ((328, RTCarData), (212, RTLapData), (408, handshackerResponse), ),
    }