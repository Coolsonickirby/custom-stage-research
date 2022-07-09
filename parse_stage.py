import struct, json

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

data_types = {
    0x01:	"byte",
    0x08:	"int",
    0x0C:	"short",
    0x0A:	"float",
    0x16:	"array of floats"
}

test_file = "stage_grass.bin"

data = open(test_file, "rb")
stage_info = {}
sted_info = {}

stage_info["stage_id"] = struct.unpack("<I", data.read(4))[0]
stage_info["version_id"] = struct.unpack("<I", data.read(4))[0]
stage_info["unk1"] = struct.unpack(">I", data.read(4))[0]
stage_info["unk_upload_flag"] = struct.unpack(">h", data.read(2))[0]
stage_info["unk_upload_value1"] = int.from_bytes(data.read(1), byteorder="big")
stage_info["unk_upload_value2"] = int.from_bytes(data.read(1), byteorder="big")
stage_info["upload_id"] = struct.unpack("<I", data.read(4))[0]
stage_info["unk2"] = struct.unpack(">I", data.read(4))[0]
stage_info["unk3"] = struct.unpack(">I", data.read(4))[0]

stage_info["unk4"] = struct.unpack("<h", data.read(2))[0]
stage_info["year"] = struct.unpack("<h", data.read(2))[0]
stage_info["month"] = int.from_bytes(data.read(1), byteorder="big")
stage_info["day"] = int.from_bytes(data.read(1), byteorder="big")
stage_info["hour"] = int.from_bytes(data.read(1), byteorder="big")
stage_info["minute"] = int.from_bytes(data.read(1), byteorder="big")
stage_info["second"] = int.from_bytes(data.read(1), byteorder="big")

# Padding?
data.read(1)

stage_info["creator_name"] = data.read(0x54).decode("utf-16").replace("\x00", "")
stage_info["country_code"] = data.read(2).decode("ansi")
stage_info["unk5"] = struct.unpack("<I", data.read(4))[0]
stage_info["creator_id2"] = struct.unpack("<Q", data.read(8))[0]

data.seek(0xC4, 0) # Absolute seeking to 0xC4

data.read(0x44)
# stage_info["unk6"] = data.read(0x44)
stage_info["stage_hash"] = struct.unpack("<I", data.read(4))[0]
stage_info["stage_name_length"] = struct.unpack("<I", data.read(4))[0] * 2
stage_info["stage_name"] = data.read(stage_info["stage_name_length"]).decode("utf-16").replace("\x00", "")


data.seek(0x134, 0) # Absolute seeking to 0xC4

stage_info["stage_size"] = struct.unpack("<I", data.read(4))[0]
stage_info["stage_background"] = struct.unpack("<I", data.read(4))[0]
stage_info["unk_stage_element"] = struct.unpack("<h", data.read(2))[0]
stage_info["unk_stage_element2"] = struct.unpack("<h", data.read(2))[0]

stage_info["stage_bgm"] = hex(struct.unpack("<Q", data.read(8))[0])
stage_info["stage_id_plus_1?"] = struct.unpack("<I", data.read(4))[0]
stage_info["stage_id_related?"] = struct.unpack("<I", data.read(4))[0]
stage_info["stage_speed"] = struct.unpack("<f", data.read(4))[0]
stage_info["unk7"] = struct.unpack("<h", data.read(2))[0]
stage_info["unk8"] = struct.unpack("<h", data.read(2))[0]
stage_info["unk_count"] = struct.unpack("<I", data.read(4))[0]
stage_info["sted_length"] = struct.unpack("<I", data.read(4))[0]
stage_info["jpeg_length"] = struct.unpack("<I", data.read(4))[0]

# with open("header_local.json", "w+") as f:
#     json.dump(stage_info, f, indent=4)

# data.close()
# exit()
# Seek to beginning of STED
sted_start_pos = 0x198
data.seek(sted_start_pos, 0)
sted_info["magic"] = data.read(4).decode("ansi")
sted_info["length"] = struct.unpack("<I", data.read(4))[0]
sted_info["ver_minor"] = struct.unpack("<h", data.read(2))[0]
sted_info["ver_major"] = struct.unpack("<h", data.read(2))[0]
sted_info["node_table_offset"] = struct.unpack("<I", data.read(4))[0]
sted_info["node_table_count"] = struct.unpack("<I", data.read(4))[0]
sted_info["node_table"] = []
sted_info["hash_table_offset"] = struct.unpack("<I", data.read(4))[0]
sted_info["hash_table_count"] = struct.unpack("<I", data.read(4))[0]
sted_info["hash_table"] = []

data.seek(sted_start_pos + sted_info["hash_table_offset"], 0)
for x in range(sted_info["hash_table_count"]):
    sted_info["hash_table"].append({
        "crc32": struct.unpack("<I", data.read(4))[0],
        "length": struct.unpack("<I", data.read(4))[0]
    })

data.seek(sted_start_pos + sted_info["node_table_offset"], 0)
for x in range(sted_info["node_table_count"]):
    node = {
        "name": struct.unpack("<h", data.read(2))[0],
        "parent_node_id": struct.unpack("<h", data.read(2))[0],
        "field_count": struct.unpack("<I", data.read(4))[0],
        "fields": []
    }

    for y in range(node["field_count"]):
        field = {
            "field_type": struct.unpack("<h", data.read(2))[0],  
            "data_type": struct.unpack("<h", data.read(2))[0],
            "offset": struct.unpack("<I", data.read(4))[0],
            "data": None
        }
        node["fields"].append(field)
    sted_info["node_table"].append(node)

for node in sted_info["node_table"]:
    for field in node["fields"]:
        data_type = field["data_type"]
        data.seek(sted_start_pos + field["offset"], 0)
        if data_type == 0x01: # byte
            field["data"] = data.read(1)
        elif data_type == 0x08:
            field["data"] = struct.unpack("<I", data.read(4))[0]
        elif data_type == 0x0C:
            field["data"] = struct.unpack("<h", data.read(2))[0]
        elif data_type == 0x0A:
            field["data"] = struct.unpack("<f", data.read(4))[0]
        elif data_type == 0x16:
            arr_len = struct.unpack("<I", data.read(4))[0]
            field["data"] = []
            for z in range(arr_len):
                field["data"].append(struct.unpack("<f", data.read(4))[0])


starting_points = []
points = []
node_id = 0
for node in sted_info["node_table"]:
    hash = "0x%s" % hex(sted_info["hash_table"][node["name"]]["crc32"])[2:].upper()
    print("- Node: %s" % labels[hash] if hash in labels else hash)
    print("\t - Node ID: %s" % node_id)
    node_id += 1
    print("\t - Parent Node ID: %s" % node["parent_node_id"])
    for field in node["fields"]:
        hash = "0x%s" % hex(sted_info["hash_table"][field["field_type"]]["crc32"])[2:].upper()
        print("\t\t - Field Type: %s - Hash Len: %s" % (labels[hash] if hash in labels else hash, hex(sted_info["hash_table"][field["field_type"]]["length"])))
        print("\t\t - Data Type: %s" % data_types[field["data_type"]])
        print("\t\t - Data:", field["data"])
        # if hash == "0x5E237E06" or hash == "0x19862D80":
        #     hash = "0x%s" % hex(sted_info["hash_table"][field["data"]]["crc32"])[2:].upper()
        #     print("\t\t - Data: %s - Hash Len: %s" % (labels[hash] if hash in labels else hash, hex(sted_info["hash_table"][field["data"]]["length"])))
        print()
    print()


# Write info to file for draw.html
for node in sted_info["node_table"]:
    hash = "0x%s" % hex(sted_info["hash_table"][node["name"]]["crc32"])[2:].upper()
    if hash == "0x44CA0B23": # Piece
        matrix = node["fields"][2]["data"]
        starting_points.append([matrix[-4], matrix[-3]])
    elif hash == "0x87C331C7": # Properties
        points.append(node["fields"][0]["data"])

with open("data.json", "w+") as f:
    json.dump({
        "starting_points": starting_points,
        "points_src": points
    }, f, indent=4)

# Seek to beginning of JPEG and extract it
data.seek(0xC998, 0)
with open('test.jpg', "w+b") as f:
    f.write(data.read(stage_info["jpeg_length"]))

# print(sted_info)
data.close()