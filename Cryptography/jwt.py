# A small project to try and generate JWTs (using RS256) using a bespoke program rather than an external library.

import os
import base64
from pem_decoder import parseFile

TEST = os.getenv("TEST")
print(TEST)

# print(parseFile(os.getenv("PUBLIC_KEY_FILE")))

HEADER = {"alg": "RS256", "typ": "JWT"}
header_b64 = base64.b64encode(str(HEADER).encode("utf-8")).decode("utf-8")
# test = {"userId": "123456", "name": "John Smith", "exp": 1788881561}

# b64 = base64.b64encode(str(HEADER).encode("ascii")).decode("ascii")
# print(str(header).encode("ascii"))
# print(b64)
# print(base64.b64decode(b64.encode("utf-8")).decode("utf-8"))

def generateJWT(payload: dict[str, str]):
    payload_b64 = base64.b64encode(str(payload).encode("utf-8")).decode("utf-8")
    message = header_b64 + "." + payload_b64
    raise NotImplementedError
    # TODO: Implement SHA256 hashing, then encrypt with RSA using pem_decoder.py to find the keys
    # TODO: JWT signature verifier

# print(generateJWT(test))