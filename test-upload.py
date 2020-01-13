import os
import http.client
from http import HTTPStatus
import json
from hashlib import sha256

MEGABYTES_TO_BYTES = 1024 * 1024

def generate_file(filename, sizeInMegabytes):
    f = open(filename, "wb")
    f.seek((sizeInMegabytes * MEGABYTES_TO_BYTES) - 1)
    f.write(bytearray([1]))
    f.close()
    pass

temp_filename = 'temp_file.dat'

generate_file(temp_filename, 100)

file = open(temp_filename, 'rb')
file_contents = file.read()
sha256_hash = sha256()
# Read and update hash string value in blocks of 4K
file.seek(0, 0)
for byte_block in iter(lambda: file.read(4096), b""):
    sha256_hash.update(byte_block)


checksum = sha256_hash.hexdigest()
print("sha256 checksum = " + checksum)

conn = http.client.HTTPSConnection("build-uploader.projectathena.io:443")

context = json.loads(os.environ['GITHUB_CONTEXT'])

owner_and_repository = context["repository"].split("/")
owner = owner_and_repository[0]
repository = owner_and_repository[1]

headers = {
    "owner": owner,
    "repo": repository,
    "check_run_id": 379467820
}

conn.request("PUT", "/", body=file_contents, headers=headers)
response = conn.getresponse()

if (response.status == HTTPStatus.OK):
    print("response: ",  json.loads(response.read()))
else:
    print(response.status, response.reason, response.read())
