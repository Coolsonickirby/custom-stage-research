import struct, json, zlib

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

handle.close()