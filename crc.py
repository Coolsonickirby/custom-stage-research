import zlib
print(hex(zlib.crc32("Grass".encode("utf-16-le")) & 0xffffffff))
