# Standardized-Telemetry-Package

A single telemetry package that can extract UDP data from multiple racing games including: <br>
F1 2024, BeamNG Drive, Project Cars 2, Forza Horizon 4, Forza Horizon 5, Forza Motorsport 7, Forza Motorsport 8, Gran Turismo 7, and Assetto Corsa.

## Features

- Unified package for multiple racing game telemetry protocols
- Support for both single-threaded and multi-threaded operation modes
- Extensible packet structure system for adding new games
- Real-time UDP data reception and decoding
- Thread-safe data storage for concurrent access

## Architecture

The multi-threaded system uses the following architecture:

- **Main Thread**: Creates and manages the telemetry system, starts worker threads, waits for stop signal
- **Network Listener Thread**: Continuously receives UDP packets, decodes them according to the game protocol, and stores the latest data in `CentralStorage`
- **Worker Threads**: User-defined threads that access telemetry data via read-only snapshots, preventing accidental data mutation

Data is stored in `CentralStorage` with thread-safe locking mechanisms. Worker threads receive a `ReadOnlyStorage` interface that only allows taking immutable snapshots, ensuring thread safety without requiring manual locking.

## Options

### Single-Threaded Mode

The single-threaded mode provides a simple, blocking function that listens for UDP packets and returns decoded telemetry data. This is suitable for applications that don't require concurrent processing or real-time worker threads.

Located in `main/support/server.py`, the `telemetryManager.get_telemetry()` function:
- Blocks until a packet is received
- Decodes the packet according to the game's protocol
- Returns the processed telemetry data
- No threading overhead, simpler for basic usage

### Multi-Threaded Mode

The multi-threaded mode runs a full telemetry server with separate threads for network listening and data processing. This allows for real-time data processing while continuously receiving new packets.

Located in `main/support/server.py`, the `telemetryManager.StartTelemetry()` class:
- Starts a network listener thread that continuously receives UDP data
- Provides a thread-safe central storage system (`CentralStorage`) for data
- Allows multiple worker threads to process data concurrently via read-only access
- Manages thread lifecycle with proper startup and shutdown procedures

## Setup

### Prerequisites

- Python 3.8+
- Access to UDP telemetry data from supported racing games



### Single-Threaded Setup

For basic telemetry extraction without threading: <br>
See `test_programs` for more single thread examples.

```python
from data_structures.f1_2024_struct import MetaData
from support.server import telemetryManager

telemetry = telemetryManager()
# telemetry.isMultiThreaded(False) # currently does nothing
telemetry.updateMeta(MetaData)

for packet, packetID, headerPacket in telemetry.get_telemetry():
    if not packet:
        continue

    # Check packetID, if available
    if packetID == 6:
        pass # Process data here

    # Check packet name
    if packetName == 'PacketCarTelemetryData'
        pass # Process data here
```

### Multi-Threaded Setup

For real-time telemetry processing with multiple threads:<br>
See `test_programs` for more multi thread examples.

```python
from data_structures.f1_2024_struct import MetaData
from support.server import telemetryManager

# Define a worker thread function
def my_worker_thread(worker_id: int, ro_storage, stop_event):
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()
        
        # Access telemetry data
        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("PacketCarTelemetryData")
            if telemetry:
                # Process data here
                pass

# Initialize the class
activeThreads = telemetryManager()

# Configure metadata and network settings
activeThreads.updateMeta(MetaData)

activeThreads.updateLocalIP("127.0.0.1") # Optional. Defaults to 0.0.0.0
# activeThreads.updateSendIP("192.168.1.100")  # Optional: for heartbeat destination

activeThreads.addWorkerThread(my_worker_thread)

activeThreads.StartTelemetry()
```


## Adding and Using a New Packet Structure

### Step 1: Create the Packet Structure File

Create a new file in `main/data_structures/` following the naming convention `{game}_struct.py`.

Example structure:

```python
from enum import Enum
# Swap depending on what data types you want to use
import ctypes 

class DataTypes(Enum):
    STRUCTURE = ctypes.LittleEndianStructure
    UNION = ctypes.Union
    
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT16 = ctypes.c_int16
    
    UNSIGNED_INT8 = ctypes.c_uint8
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT32 = ctypes.c_uint32
    UNSIGNED_INT64 = ctypes.c_uint64
    
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    DOUBLE = ctypes.c_double

# Define your header packet, if required
class PacketHeader(DataTypes.STRUCTURE.value):
    _pack_ = 1 # This may be required depening on the game
    _fields_ = [
        ("m_packetFormat",              DataTypes.UNSIGNED_INT16.value),
        ("m_gameYear",                  DataTypes.UNSIGNED_INT8.value),
        ("m_gameMajorVersion",          DataTypes.UNSIGNED_INT8.value),
        ("m_gameMinorVersion",          DataTypes.UNSIGNED_INT8.value),
        ("m_packetVersion",             DataTypes.UNSIGNED_INT8.value),
        ("m_packetId",                  DataTypes.UNSIGNED_INT8.value),
        ("m_sessionUID",                DataTypes.UNSIGNED_INT64.value),
        ("m_sessionTime",               DataTypes.FLOAT.value),
        ("m_frameIdentifier",           DataTypes.UNSIGNED_INT32.value),
        ("m_overallFrameIdentifier",    DataTypes.UNSIGNED_INT32.value),
        ("m_playerCarIndex",            DataTypes.UNSIGNED_INT8.value),
        ("m_secondaryPlayerCarIndex",   DataTypes.UNSIGNED_INT8.value),
    ]

# Define any sub-packet
class CarMotionData(DataTypes.STRUCTURE.value):
    # _pack_ = 1 # This may be required depening on the game
    _fields_ = [
        ("m_worldPositionX",        DataTypes.FLOAT.value),
        ("m_worldVelocityX",        DataTypes.FLOAT.value),
        ("m_worldForwardDirX",      DataTypes.SIGNED_INT16.value),
        ("m_worldRightDirX",        DataTypes.SIGNED_INT16.value),
        ("m_gForceLateral",         DataTypes.FLOAT.value),
        # ...
    ]

# Define a main packet
class PacketMotionData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # This may be required depening on the game
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carMotionData", CarMotionData * 22),    # Data for all cars on track
    ]

```

### Step 2: Setup MetaData

In your main script, import the new metadata:

| Syntax            | Type              | Description |
| ----------------- | ----------------- | ------------|
| port              | Integer           | UDP port data is received on
| fullBufferSize    | Integer           | Maximum packet size
| heartBeatPort     | Integer           | UDP port to send a heart beat to
| heartBeatFunc     | Function          | Heart beat function
| handShakePort     | Integer           | UDP port to send a hand shake to
| handShakeFunc     | Tuple [Function, Function] | Tuple containing start and stop hand shake functions
| decrytionFunc     | Function          | Data decryption function
| headerInfo        | Tuple [int, type] | Tuple containing, the packet size and header struct class (if protocol uses header).
| packetIDAttribute | String            | An attribute in the header packet defining the packet ID
| packetInfo        | Dict [int, List [Same as headerInfo] ]    | Game packet mapping - See more below

#### PacketInfo

A Dictionary containing
- key: Packet ID or 0 if no ID
- value: Tuple of (packetSize, packetStructClass) variants.

#### PacketInfo - Standard
```python
packetInfo = {
    0: ((1349, PacketMotionData),),
    1: ((753, PacketSessionData),),
    # ...
}
```

#### PacketInfo - PacketID with multiple packets
```python
packetInfo = {
    0: ((559, TelemetryData),),
    7: ((1040, TimeStatsData),),
    8: ((1452, VehicleClassNamesData), (1164, ParticipantVehicleNamesData),),
    # ...
}
```

#### PacketInfo - No PacketID
```python
packetInfo = {
    0: ((296, PacketAData), (316, PacketBData), (344, PacketTildaData), (368, PacketCData)),
    # ...
}
```

#### Full MetaData Example

``` python
# MetaData class with packet information
class MetaData:
    # standard network info
    port: int = 20777  # UDP port for your game
    fullBufferSize: int = 1464  # Maximum packet size

    # use if a heartbeat is needed
    heartBeatPort = 33739
    heartBeatFunc = heartBeat

    # use for itinial hand shake
    handShakePort = None
    handShakeFunc = None # tuple (startHandShakeFunc, stopHandShakeFunc)

    # use if the data needs decrypting
    decrytionFunc = decrypt_data

    # use if there is a header packet
    headerInfo: tuple[int, type] = (32, PacketHeader)  # Header size and type
    packetIDAttribute: str = "m_packetId"  # Attribute name for packet ID

    # standard packet info
    packetInfo: dict[int, tuple[tuple[int, type], ...]] = {
        0: ((1349, PacketMotionData),),  # Packet ID: ((size, packet_class),)
        # Add more packet types as needed
    }
```

### Step 3: Import and Use

In your main script, import the new metadata and use it with either mode:

```python
from data_structures.your_game_struct import MetaData as YourGameMetaData
from support.server import telemetryManager

## Setup for both modes
activeThreads = telemetryManager()
activeThreads.updateMeta(YourGameMetaData)

## Use in single-threaded mode
for packet, packetID, headerPacket in telemetry.get_telemetry():
    if not packet:
        continue

## Or in multi-threaded mode
activeThreads.addWorkerThread(your_worker_function)
activeThreads.StartTelemetry()
```

### Step 4: Handle Packet Decoding

The system automatically handles packet decoding based on the `packetInfo` dictionary. Ensure:
- Packet sizes match exactly (use `_pack_ = 1` for correct alignment)
- Packet IDs correspond to the correct packet types
- All nested structures are properly defined

## Supported Games

- Assetto Corsa
- BeamNG Drive
- F1 2024
- Forza Horizon 4
- Forza Horizon 5
- Forza Motorsport 7 (untested)
- Forza Motorsport 8
- Gran Turismo 7
- Project Cars 2

## Troubleshooting

- Check that the game is configured to send telemetry data
- Check no other running game uses the same port (on xbox, if a game is in quick resume state, it may block access to a port. EG; forza horizon 5 and motorsport 8) 
- Verify IP addresses are correctly configured for network communication
- Use packet capture tools to verify data transmission (wireshark, and filter based on UDP, port, incoming and source IP)
- Ensure firewall allows UDP traffic on the configured port
- For Microsoft Store versions of Forza games, ensure loopback is configured correctly (see `forza debug.txt` in supporting docs)

## Support Documentation

Additional documentation and debugging guides are available in the `Supporting Docs/` folder:

- **Data Output from F1 24 v27.2x.docx** - Detailed analysis of packet structures and data output for F1 2024 version 27.2x (official release)
- **forza debug.txt** - Debugging setup for Forza games including local loopback configuration for Microsoft Store versions
