# Given a PEM encoded RSA key (with no headers and whitespace removed), return the exponent and modulus contained in the data.

import os
import base64

key = os.getenv("PUBLIC_KEY")
# print(key)
print(base64.b64decode(key.encode("utf-8")))

# Iteration works per byte. The bytes starting \x are those without a Unicode character