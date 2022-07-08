import struct
test_paths = [
    "C:\\Users\\Random\\Downloads\\stage_Green_Hill_Boss.bin",
    "C:\\Users\\Random\\Downloads\\stage_COME_TO_BRAZIL.bin",
    "C:\\Users\\Random\\Downloads\\stage_Reposting_Doots.bin",
    "C:\\Users\\Random\\Downloads\\stage_Sheep.bin"
]


labels = {
    "0xC1E965DC": "__root",
    "0x5E237E06": "name",
    "0x595CEB81": "rail",
    "0x21D4778E": "switch",
    "0x44CA0B23": "piece",
    "0x7119107A": "ground",
    "0x0B44539B": "gear",
    "0xE8058B83": "global",
    "0x4487E306": "seed",
    "0xCCF1F1BA": "editor",
    "0x3BC4BCD9": "kind",
    "0xF83341CF": "matrix",
    "0xB7208209": "parent_matrix",
    "0x466F2FFC": "target",
    "0x37BDBC25": "ladder",
    "0x6B3E1469": "spring",
    "0xFEF0A831": "bumper",
    "0x4A2FDF87": "cannon",
    "0xA97F91D7": "ignition",
    "0xD3B58C66": "warp",
    "0x210B54FE": "wind",
    "0x87C331C7": "properties",
    "0x7DF9A055": "causingexplosion",
}

data_types = [
    0x01,
    0x08,
    0x0C,
    0x0A,
    0x16,
]

test_path = test_paths[0]
info = {}

handle = open(test_path, "rb")

sted_start_pos = 0x198
handle.seek(sted_start_pos, 0)
info["magic"] = handle.read(4).decode("ansi")
info["length"] = struct.unpack("<I", handle.read(4))[0]
info["ver_minor"] = struct.unpack("<h", handle.read(2))[0]
info["ver_major"] = struct.unpack("<h", handle.read(2))[0]
info["node_table_offset"] = struct.unpack("<I", handle.read(4))[0]
info["node_table_count"] = struct.unpack("<I", handle.read(4))[0]
info["node_table"] = []
info["hash_table_offset"] = struct.unpack("<I", handle.read(4))[0]
info["hash_table_count"] = struct.unpack("<I", handle.read(4))[0]
info["hash_table"] = []

handle.seek(sted_start_pos + info["hash_table_offset"], 0)
for x in range(info["hash_table_count"]):
    info["hash_table"].append({
        "crc32": struct.unpack("<I", handle.read(4))[0],
        "length": struct.unpack("<I", handle.read(4))[0]
    })

handle.seek(sted_start_pos + info["node_table_offset"], 0)
for x in range(info["node_table_count"]):
    node = {
        "name": struct.unpack("<h", handle.read(2))[0],
        "parent_node_id": struct.unpack("<h", handle.read(2))[0],
        "field_count": struct.unpack("<I", handle.read(4))[0],
        "fields": []
    }

    for y in range(node["field_count"]):
        field = {
            "field_type": struct.unpack("<h", handle.read(2))[0],  
            "data_type": struct.unpack("<h", handle.read(2))[0],
            "offset": struct.unpack("<I", handle.read(4))[0],
            "data": None
        }
        node["fields"].append(field)
    info["node_table"].append(node)

for node in info["node_table"]:
    for field in node["fields"]:
        data_type = field["data_type"]
        handle.seek(sted_start_pos + field["offset"], 0)
        if data_type == 0x01: # byte
            field["data"] = handle.read(1)
        elif data_type == 0x08:
            field["data"] = struct.unpack("<I", handle.read(4))[0]
        elif data_type == 0x0C:
            field["data"] = struct.unpack("<h", handle.read(2))[0]
        elif data_type == 0x0A:
            field["data"] = struct.unpack("<f", handle.read(4))[0]
        elif data_type == 0x16:
            arr_len = struct.unpack("<I", handle.read(4))[0]
            field["data"] = []
            for z in range(arr_len):
                field["data"].append(struct.unpack("<f", handle.read(4))[0])

for node in info["node_table"]:
    hash = "0x%s" % hex(info["hash_table"][node["name"]]["crc32"])[2:].upper()
    print(labels[hash] if hash in labels else hash)

handle.close()