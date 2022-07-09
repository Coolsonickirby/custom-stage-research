import struct, json

with open("header_local.json", "r") as f:
    stage_data = json.load(f)

handle = open("stage_python.bin", "w+b")

stage_info = stage_data["stage_info"]

handle.write(struct.pack("<I", stage_info["stage_id"]))
handle.write(struct.pack("<I", stage_info["version_id"]))
handle.write(struct.pack(">I", 0)) # Write unk1
handle.write(struct.pack(">h", 0)) # Write unk_upload_flag
handle.write((1).to_bytes(1, byteorder='big')) # Write unk_upload_value1
handle.write((1).to_bytes(1, byteorder='big')) # Write unk_upload_value2
handle.write(struct.pack("<I", 0)) # Write Upload ID
handle.write(struct.pack(">I", 0)) # Write unk2
handle.write(struct.pack(">I", 0)) # Write unk3
# stage_info["stage_id"] = struct.unpack("<I", data.read(4))[0]
# stage_info["version_id"] = struct.unpack("<I", data.read(4))[0]
# stage_info["unk1"] = struct.unpack(">I", data.read(4))[0]
# stage_info["unk_upload_flag"] = struct.unpack(">h", data.read(2))[0]
# stage_info["unk_upload_value1"] = int.from_bytes(data.read(1), byteorder="big")
# stage_info["unk_upload_value2"] = int.from_bytes(data.read(1), byteorder="big")
# stage_info["upload_id"] = struct.unpack("<I", data.read(4))[0]
# stage_info["unk2"] = struct.unpack(">I", data.read(4))[0]
# stage_info["unk3"] = struct.unpack(">I", data.read(4))[0]



handle.write(struct.pack("<h", stage_info["date"]["unk4"])) # Write unk4
handle.write(struct.pack("<h", stage_info["date"]["year"])) # Write Year
handle.write((stage_info["date"]["month"]).to_bytes(1, byteorder='big')) # Write Month
handle.write((stage_info["date"]["day"]).to_bytes(1, byteorder='big')) # Write Day
handle.write((stage_info["date"]["hour"]).to_bytes(1, byteorder='big')) # Write Hour
handle.write((stage_info["date"]["minute"]).to_bytes(1, byteorder='big')) # Write Minute
handle.write((stage_info["date"]["second"]).to_bytes(1, byteorder='big')) # Write Second
# stage_info["unk4"] = struct.unpack("<h", data.read(2))[0]
# stage_info["year"] = struct.unpack("<h", data.read(2))[0]
# stage_info["month"] = int.from_bytes(data.read(1), byteorder="big")
# stage_info["day"] = int.from_bytes(data.read(1), byteorder="big")
# stage_info["hour"] = int.from_bytes(data.read(1), byteorder="big")
# stage_info["minute"] = int.from_bytes(data.read(1), byteorder="big")
# stage_info["second"] = int.from_bytes(data.read(1), byteorder="big")

handle.write((0).to_bytes(1, byteorder='big')) # Write unk_upload_value2

creator_name = stage_info["creator_name"].encode("utf-16-le")
handle.write(creator_name)
if len(creator_name) < 0x54:
    handle.write((0).to_bytes(0x54 - len(creator_name), byteorder='big')) # Write unk_upload_value2
    

# stage_info["creator_name"] = data.read(0x54).decode("utf-16").replace("\x00", "")
# stage_info["country_code"] = data.read(2).decode("ansi")
# stage_info["unk5"] = struct.unpack("<I", data.read(4))[0]
# stage_info["creator_id2"] = struct.unpack("<Q", data.read(8))[0]


handle.close()