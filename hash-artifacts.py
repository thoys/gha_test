import os
import json
from hashlib import sha256

FILE_READ_BUFFER = 4096

temp_filename = 'temp_file.dat'
file = open(temp_filename, 'rb')
file_contents = file.read()
sha256_hash = sha256()

file.seek(0, 0)
for byte_block in iter(lambda: file.read(FILE_READ_BUFFER), b""):
    sha256_hash.update(byte_block)

checksum = sha256_hash.hexdigest()

uploading_files = []

uploading_files.append({
    "filename": temp_filename,
    "sha256_checksum": checksum
})

print("BuildFileHashes: " + json.dumps(uploading_files))
