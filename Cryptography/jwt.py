# A small project to try and generate JWTs (using RS256) using a bespoke program rather than external libraries.

import os

TEST = os.getenv("TEST")
print(TEST)

header = {"alg": "RS256", "typ": "JWT"}
payload = {"userId": "123456", "name": "John Smith", "exp": 1788881561}

import base64

b64 = base64.b64encode(str(header).encode("ascii")).decode("ascii")
# print(str(header).encode("ascii"))
print(b64)
print(base64.b64decode(b64.encode("utf-8")).decode("utf-8"))