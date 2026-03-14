import ctypes


def expand(packet, tyre=False):
    tempList = []
    tempDict = {}
    tyres = ["RL", "RR", "FL", "FR"]
    if tyre:
        for x in range(len(packet)):
            name = f"{tyre}_{tyres[x]}"
            tempDict[name] = round(packet[x], 5)
        return tempDict
    else:
        for x in range(len(packet)):
            tempList.append(packet[x])

        return tempList


def split(value) -> list:
    involved = []
    lst = [1]
    while len(lst) <= 31:
        lst.append(int(lst[-1:][0]) * 2)
    for x in reversed(lst):
        newValue = value - x
        if value - x < 0:
            continue
        value = newValue
        involved.append(x)
    if involved:
        return involved
    return [0]


def newChrToString(value, extra=True):
    if extra:
        return bytes(value).decode("utf-8").strip("\0").split("\x00", 1)[0]
    else:
        return bytes(value).decode("utf-8").strip("\0")


def dynamic_ingest(packet):
    attrs = {field[0]: getattr(packet, field[0]) for field in packet._fields_}

    packetName = packet.__class__.__name__

    newPacket = type(packetName, (), {})

    for source_attr, value in attrs.items():

        if isinstance(value, bytes):
            value = newChrToString(value)

        elif isinstance(value, float):
            value = round(value, 5)

        elif isinstance(value, ctypes.Array):
            value = list(value)

            for key, item in enumerate(value):
                if type(item) in [int, str]:
                    pass

                elif isinstance(item, float):
                    value[key] = round(item, 5)

                elif isinstance(item, ctypes.Array):
                    value[key] = newChrToString(item)

                else:
                    # assume it is a class
                    value[key] = dynamic_ingest(item)

        elif type(value) not in [int, str]:
            # print("Unrecognised type or assuming it is a class")
            value = dynamic_ingest(value)
            # continue

        setattr(newPacket, source_attr, value)

    return newPacket
