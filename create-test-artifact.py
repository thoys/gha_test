import json
import time
import struct
import random


print("Creating test artifact.")

MEGABYTES_TO_BYTES = 1024 * 1024

def generate_file(filename, sizeInMegabytes):
    f = open(filename, "wb")
    # add time at front
    f.write(bytearray(struct.pack("f", time.time())))
    # add some random value to get unique files
    f.write(bytearray(random.getrandbits(8) for _ in range(32)))
    f.seek((sizeInMegabytes * MEGABYTES_TO_BYTES) - 1)
    f.write(bytearray([1]))
    f.close()
    pass

generate_file('temp_file.dat', 100)

print("Test artifact created.")
