import os
import http.client
from http import HTTPStatus
import json
from hashlib import sha256
import time
import struct
import random

MEGABYTES_TO_BYTES = 1024 * 1024
FILE_READ_BUFFER = 4096

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

temp_filename = 'temp_file.dat'

generate_file(temp_filename, 100)

file = open(temp_filename, 'rb')
file_contents = file.read()
sha256_hash = sha256()

file.seek(0, 0)
for byte_block in iter(lambda: file.read(FILE_READ_BUFFER), b""):
    sha256_hash.update(byte_block)


checksum = sha256_hash.hexdigest()
print("sha256 checksum = " + checksum)

uploading_files = []

uploading_files.append({
    "filename": temp_filename,
    "sha256_checksum": checksum
})

print("BuildFileHashes: " + json.dumps(uploading_files))

conn = http.client.HTTPSConnection("build-uploader.projectathena.io")

context = json.loads(os.environ['GITHUB_CONTEXT'])

owner_and_repository = context["repository"].split("/")
owner = owner_and_repository[0]
repository = owner_and_repository[1]

headers = {
    "owner": owner,
    "repo": repository,
    "commit_hash": context["event"]["sha"],
    "pull_number": context["event"]["number"],
    "job_name": os.environ['JOB_NAME']
}

conn.request("PUT", "/", body=file_contents, headers=headers)
response = conn.getresponse()

if (response.status == HTTPStatus.OK):
    print("response: ",  json.loads(response.read()))
else:
    print(response.status, response.reason, response.read())
