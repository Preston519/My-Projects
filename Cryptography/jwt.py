# A small project to try and generate JWTs (using RS256) using a bespoke program rather than an external library.

import os
import b64
from pem_decoder import parse_file
from sha256 import sha256

def dict_to_json(val: dict):
    return b64.url_encode(str(val).replace("'", '"').replace(", ", ",").replace(": ", ":").encode("utf-8"))

HEADER = {"alg": "RS256", "typ": "JWT"}
header_b64 = dict_to_json(HEADER)


def generateJWT(payload: dict[str, str]):
    payload_b64 = dict_to_json(payload)
    message = header_b64 + "." + payload_b64
    d, n = parse_file(os.getenv("PRIVATE_KEY_FILE"))
    encrypted = pow(int.from_bytes(sha256(message).encode("utf-8")), d, n)
    signature = b64.url_encode(encrypted.to_bytes(256))
    return message + "." + signature

# TODO: JWT signature verifier

if __name__ == "__main__":
    test = {"userId": "123456", "name": "John Smith", "exp": 1788881561}
    print(generateJWT(test))
    # print(header_b64)
    # print(str(HEADER).replace("'", '"').replace(", ", ",").replace(": ", ":").encode("utf-8"))
    # print(b64.encode(str(HEADER).encode("utf-8")))
    # import base64
    # print(base64.urlsafe_b64encode(str(HEADER).encode("utf-8")))