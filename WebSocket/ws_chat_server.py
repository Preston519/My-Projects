# Server for chat app. Ideally this would be hosted with an SSL certificate so JWTs and passwords can be securely transmitted

import websockets
import asyncio
import json
import time
import csv
from http import HTTPStatus
import os
import bcrypt

connections = set()

async def send_message(message):
    async with websockets.connect("wahh") as ws:
        await ws.send(message)
        
async def handler(connection: websockets.ClientConnection): # Handler for a connected client
    print("Client connected")
    connections.add(connection)
    
    # info = json.loads(await connection.recv())
    # username = info["username"]
    # colour = info["colour"]
    
    # First message should be the auth token
    authmsg = json.loads(await connection.recv())
    if not authmsg["type"] == "auth":
        connection.close()
        return
    if not verifyJWT(authmsg["token"]):
        await connection.send(json.dumps({"type": "auth", "success": "false", "reason": "Invalid auth token"}))
        connection.close()
        return
    elif check_token_expired(authmsg["token"]):
        await connection.send(json.dumps({"type": "auth", "success": "false", "reason": "Auth token expired"}))
        connection.close()
        return
    
    # TODO: search database for user details. JWT should contain uid as primary key
    # await connection.send(json.dumps({"type": "auth", "success": "true", "username"}))
    
    with open("chat-history/chat.csv", "r", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            await connection.send(json.dumps(row))

    filename = "chat-history/chat.csv"
    async for message in connection:
        print(f"Received message: {message}")
        timestamp = int(time.time())
        with open(filename, "a", newline='') as file:
            csv.writer(file, quoting=csv.QUOTE_MINIMAL).writerow([username, colour, message, timestamp])
        async with asyncio.TaskGroup() as tgroup:
            for user in connections:
                tgroup.create_task(user.send(json.dumps({"type": "message", "username": username, "colour": colour, "message": message, "time": timestamp})))
    connections.remove(connection)
    print("Client disconnected")
    
async def process_request(connection: websockets.ServerConnection, request: websockets.Request):
    if request.path == "/login":
        username = request.headers.get("X-Username")
        password = request.headers.get("X-Password")
        # TODO: Validate username and password
        valid = True
        if valid:
            # TODO: Generate auth token
            token = "Placeholder" # REPLACE
            response =  connection.respond(HTTPStatus.OK, '{"success":"true","token":"{}"}'.format(token))
        else:
            response = connection.respond(HTTPStatus.UNAUTHORIZED, '{"success":"false"}')
        response.headers["Content-Type"] = "application/json"
        return response
    elif request.path == "/auth":
        token = request.headers.get("X-JWT")
        if verifyJWT(token):
            response = connection.respond(HTTPStatus.OK, '{"success":"true"}')
        else:
            response = connection.respond(HTTPStatus.UNAUTHORIZED, '{"success":"false"}')
        response.headers["Content-Type"] = "application/json"
        return response
    return None

async def main():
    server = await websockets.serve(handler, "localhost", 8080, process_request=process_request)
    print("Server online")
    await server.serve_forever()
    print("Server offline")
    
def check_token_expired(token: str):
    try:
        t = token.index(".")+1
        payload = json.loads(url_decode(token[t : token.index(".", t)]))
        return payload["exp"] < int(time.time())
    except:
        return True
        
if __name__ == "__main__":
    asyncio.run(main())
    
    
    
    
    
    
    
# Stuff copied from other folders
CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def url_encode(bstring: bytes):
    return encode(bstring).replace("+", "-").replace("/", "_").rstrip("=")

def url_decode(string: str):
    return decode(string.replace("-", "+").replace("_", "/") + (4 - len(string) % 4) * "=")

def decode(string: str):
    if len(string) % 4:
        raise ValueError("Invalid b64 string")
    elif type(string) != str:
        raise TypeError("string should be of type str")
    if len(string) == 0:
        return ""
    res = b""
    for i in range(0, len(string)-4, 4):
        acc = 0
        for j in range(4):
            acc = (acc << 6) + CHARSET.index(string[i+j])
        res += acc.to_bytes(3)
    three = CHARSET.index(string[-3])
    res += (CHARSET.index(string[-4]) << 2 | three >> 4).to_bytes()
    if string[-2] != "=":
        two = CHARSET.index(string[-2])
        res += ((three & 0xf) << 4 | two >> 2).to_bytes()
        if string[-1] != "=":
            res += ((two & 0x3) << 6 | CHARSET.index(string[-1])).to_bytes()
    return res

def encode(bstring: bytes):
    res = ""
    for i in range(0, len(bstring)-2, 3):
        n = int.from_bytes(bstring[i:i+3])
        res += "".join(CHARSET[n >> j & 0x3f] for j in range(18, -1, -6))
    suff = len(bstring) % 3
    if suff != 0:
        n = int.from_bytes(bstring[-suff:]) << (3 - suff) * 2
        res += "".join(CHARSET[n >> j & 0x3f] for j in range(suff * 6, -1, -6)) + "=" * (3 - suff)
    return res

k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

def sha256(message: str):
    if len(message) >= 1 << 62:
        raise ValueError("Message above size limit")
    h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
    chunks = []
    acc = 0
    n = 0
    for char in message:
        acc = (acc << 8) + ord(char)
        n += 1
        if n == 64:
            chunks.append(acc)
            acc = 0
            n = 0
        elif n > 64:
            raise AssertionError("n must be <= 64")
    if n < 56:
        acc = ((acc << 8) + 0x80 << (63 - n) * 8) + len(message) * 8
    else:
        chunks.append((acc << 8) + 0x80 << (63 - n) * 8)
        acc = len(message) * 8
    chunks.append(acc)
    for chunk in chunks:
        w = []
        for i in range(480, -1, -32):
            w.append(chunk >> i & 0xffffffff)
        for _ in range(48):
            s0 = rotate_right(w[-15], 7) ^ rotate_right(w[-15], 18) ^ w[-15] >> 3
            s1 = rotate_right(w[-2], 17) ^ rotate_right(w[-2], 19) ^ w[-2] >> 10
            w.append((s0 + s1 + w[-16] + w[-7]) % (1 << 32))
        v = h[:]
        for j in range(64):
            ch = v[4] & v[5] ^ ~v[4] & v[6]
            maj = v[0] & v[1] ^ v[0] & v[2] ^ v[1] & v[2]
            t = (v[7] + ch + k[j] + w[j] + (rotate_right(v[4], 6) ^ rotate_right(v[4], 11) ^ rotate_right(v[4], 25))) % (1 << 32)
            for m in range(7, 0, -1):
                v[m] = v[m-1]
            v[0] = (t + maj + (rotate_right(v[0], 2) ^ rotate_right(v[0], 13) ^ rotate_right(v[0], 22))) % (1 << 32)
            v[4] = (v[4] + t) % (1 << 32)
        for l in range(8):
            h[l] = (h[l] + v[l]) % (1 << 32)
    return "".join(f"{h[p]:08x}" for p in range(8))

def rotate_right(word: int, n: int):
    if n < 0:
        raise ValueError("n is negative")
    return ((word & (1 << n) - 1) << 32 - n) | (word >> n)

def parse(bstring: bytes, debug=False, depth=0):
    if not bstring:
        return (None, None)
    if bstring[1] & 0x80:
        i = 2+(bstring[1] & 0x7f)
        length = int.from_bytes(bstring[2:i])
    else:
        length = bstring[1]
        i = 2
    if len(bstring) < i+length:
        raise ValueError("Invalid tag length")
    if debug:
        print(depth*"-", hex(bstring[0]), "|", bstring[1:i], "| len", length, "| i", i)
    match bstring[0]:
        case 0x30 | 0x03 | 0x04:
            if bstring[0] == 0x03:
                i += 1
            a, b = parse(bstring[i:i+length], debug, depth+1)
        # INTEGER
        case 0x02:
            a = int.from_bytes(bstring[i:i+length])
            b = None
        case _:
            if debug:
                print("Leaf discarded with tag", hex(bstring[0]))
            a = None
            b = None
    c, d = parse(bstring[i+length:], debug, depth)
    if a == None or c != None and a < 1 << 64:
        return (c,d)
    elif b == None:
        return (a,c)
    elif c != None:
        raise ValueError("(Int, Int) needs to merge with nonempty further parse")
    else:
        return (a,b)
   
def parse_file(filepath, debug=False):
    with open(filepath, "r") as file:
        data = decode("".join(row[:-1] for row in file.readlines()[1:-1]))
    return parse(data, debug)

def verifyJWT(token: str):
    try:
        split = token.index(".", token.index(".")+1)
        n, e = parse_file(os.getenv("PUBLIC_KEY_FILE"))
        decrypted = pow(int.from_bytes(url_decode(token[split+1:])), e, n)
        hashed = int.from_bytes(sha256(token[:split]).encode("utf-8"))
        return decrypted == hashed
    except ValueError:
        return False

def dict_to_json(val: dict):
    return url_encode(str(val).replace("'", '"').replace(", ", ",").replace(": ", ":").encode("utf-8"))

HEADER = {"alg": "RS256", "typ": "JWT"}
header_b64 = dict_to_json(HEADER)

def generateJWT(payload: dict[str, str]):
    payload_b64 = dict_to_json(payload)
    message = header_b64 + "." + payload_b64
    n, d = parse_file(os.getenv("PRIVATE_KEY_FILE"))
    encrypted = pow(int.from_bytes(sha256(message).encode("utf-8")), d, n)
    signature = url_encode(encrypted.to_bytes(256))
    return message + "." + signature