import struct, json, zlib

with open("header_local.json", "r") as f:
    stage_data = json.load(f)

with open(stage_data["jpeg"], "rb") as thumb:
    thumbnail = thumb.read()

handle = open("stage_python.bin", "w+b")

stage_info = stage_data["stage_info"]
sted_info = stage_data["sted_info"]

handle.write(struct.pack("<I", stage_info["stage_id"]))
handle.write(struct.pack("<I", stage_info["version_id"]))
handle.write(struct.pack(">I", 0)) # Write unk1
handle.write(struct.pack(">h", 0)) # Write unk_upload_flag
handle.write((1).to_bytes(1, byteorder='big')) # Write unk_upload_value1
handle.write((1).to_bytes(1, byteorder='big')) # Write unk_upload_value2
handle.write(struct.pack("<I", 0)) # Write Upload ID
handle.write(struct.pack(">I", 0)) # Write unk2
handle.write(struct.pack(">I", 0)) # Write unk3


handle.write(struct.pack("<h", stage_info["date"]["unk4"])) # Write unk4
handle.write(struct.pack("<h", stage_info["date"]["year"])) # Write Year
handle.write((stage_info["date"]["month"]).to_bytes(1, byteorder='big')) # Write Month
handle.write((stage_info["date"]["day"]).to_bytes(1, byteorder='big')) # Write Day
handle.write((stage_info["date"]["hour"]).to_bytes(1, byteorder='big')) # Write Hour
handle.write((stage_info["date"]["minute"]).to_bytes(1, byteorder='big')) # Write Minute
handle.write((stage_info["date"]["second"]).to_bytes(1, byteorder='big')) # Write Second

handle.write((0).to_bytes(1, byteorder='big')) # Write unk_upload_value2

creator_name = stage_info["creator_name"].encode("utf-16-le") # Encode creator name
handle.write(creator_name) # Write creator name
if len(creator_name) < 0x54: # If creator name not long enough, then pad
    handle.write((0).to_bytes(0x54 - len(creator_name), byteorder='big')) # Pad
handle.write(stage_info["country_code"].encode("ansi")) # Write Country Code
handle.write(struct.pack("<I", 0)) # Write unk5
handle.write(struct.pack("<Q", stage_info["creator_id"]))

# Padding
handle.write((0).to_bytes(0x80, byteorder='big')) # Pad

stage_hash = zlib.crc32(stage_info["stage_name"].encode("utf-16-le")) & 0xffffffff
handle.write(struct.pack(">I", stage_hash)) # Write Stage Hash
handle.write(struct.pack("<I", len(stage_info["stage_name"]))) # Write Stage Length
stage_name = stage_info["stage_name"].encode("utf-16-le")
handle.write(stage_name)
if len(stage_name) < 0x20:
    handle.write((0).to_bytes(0x20 - len(stage_name), byteorder='big')) # Pad

handle.write(struct.pack("<I", 0)) # Write unk
handle.write(struct.pack("<I", stage_info["stage_size"])) # Write Stage Size
handle.write(struct.pack("<I", stage_info["stage_background"])) # Write Stage Background
handle.write(struct.pack("<h", 0)) # Write unk_stage_element
handle.write(struct.pack("<h", 0)) # Write unk_stage_element2

stage_bgm = int(stage_info["stage_bgm"], base=16)
handle.write(stage_bgm.to_bytes(8, byteorder='little'))
handle.write(struct.pack("<I", stage_info["stage_id"] + 1))
handle.write(struct.pack("<I", stage_info["stage_id"] + 1))

handle.write(struct.pack("<f", stage_info["stage_speed"]))
handle.write(struct.pack("<h", 1))
handle.write(struct.pack("<h", 0))
handle.write(struct.pack("<I", 1))
# write sted and jpeg sizes
# HEADER DONE!

sted_data = {
    "header": bytearray(),
    "data": bytearray(),
    "nodes_table": bytearray(),
    "hash_table": bytearray()
}

for hash40 in sted_info["hash_table"]:
    sted_data["hash_table"].extend(struct.pack("<I", hash40["crc32"]))
    sted_data["hash_table"].extend(struct.pack("<I", hash40["length"]))

for node in sted_info["nodes"]:
    # Node Name
    sted_data["nodes_table"].extend(struct.pack("<h", node["name"]))
    # Parent Node ID
    sted_data["nodes_table"].extend(struct.pack("<h", node["parent_node_id"]))
    # Field Count
    sted_data["nodes_table"].extend(struct.pack("<I", node["field_count"]))
    # Fields
    for field in node["fields"]:
        # Field Type
        sted_data["nodes_table"].extend(struct.pack("<h", field["field_type"]))
        # Data Type
        data_type = field["data_type"]
        sted_data["nodes_table"].extend(struct.pack("<h", data_type))
        # Offset (Size of header + length of current data)
        data_offset = 0x40 + len(sted_data["data"])
        sted_data["nodes_table"].extend(struct.pack("<I", data_offset))
        if data_type == 0x01:
            sted_data["data"].extend((int(field["data"])).to_bytes(1, byteorder='little'))
        elif data_type == 0x08:
            sted_data["data"].extend(struct.pack("<I", int(field["data"])))
        elif data_type == 0x0C:
            sted_data["data"].extend(struct.pack("<h", int(field["data"])))
        elif data_type == 0x0A:
            sted_data["data"].extend(struct.pack("<f", float(field["data"])))
        elif data_type == 0x16:
            sted_data["data"].extend(struct.pack("<I", len(field["data"])))
            for entry in field["data"]:
                sted_data["data"].extend(struct.pack("<f", float(entry)))

# 0x40 = Header Size
sted_length = 0x40 + len(sted_data["data"]) + len(sted_data["nodes_table"]) + len(sted_data["hash_table"])
print(sted_length)
sted_data["header"].extend("DETS".encode('ansi'))
sted_data["header"].extend(struct.pack("<I", sted_length))
sted_data["header"].extend(struct.pack("<h", 0))
sted_data["header"].extend(struct.pack("<h", 1))
sted_data["header"].extend(struct.pack("<I", 0x40 + len(sted_data["data"])))
sted_data["header"].extend(struct.pack("<I", len(sted_info["nodes"])))
sted_data["header"].extend(struct.pack("<I", 0x40 + len(sted_data["data"]) + len(sted_data["nodes_table"])))
sted_data["header"].extend(struct.pack("<I", len(sted_info["hash_table"])))
sted_data["header"].extend((0).to_bytes(0x24, byteorder='little'))


handle.write(struct.pack("<I", sted_length))
handle.write(struct.pack("<I", len(thumbnail)))
handle.write((0).to_bytes(0x34, byteorder='big')) # Pad

handle.write(sted_data["header"])
handle.write(sted_data["data"])
handle.write(sted_data["nodes_table"])
handle.write(sted_data["hash_table"])

if sted_length != 0xC800:
    handle.write((0).to_bytes(0xC800 - sted_length, byteorder='big')) # Pad

handle.write(thumbnail)

if len(thumbnail) < 0x25800:
    handle.write((0).to_bytes(0x25800 - len(thumbnail), byteorder='big')) # Pad


handle.close()