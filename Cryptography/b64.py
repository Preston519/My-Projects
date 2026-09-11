# Manually creating base 64 encoding and decoding

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

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
    for i in range(0, len(bstring)-3, 3):
        n = int.from_bytes(bstring[i:i+3])
        res += "".join(CHARSET[n >> j & 0x3f] for j in range(18, -1, -6))
    
    suff = len(bstring) % 3
    n = int.from_bytes(bstring[-suff:]) << (3 - suff) * 2
    res += "".join(CHARSET[n >> j & 0x3f] for j in range((suff) * 6, -1, -6)) + "=" * (3 - suff)
    
    return res

if __name__ == "__main__":
    TEST = "d2txbmxha3NvaSkqIDEiIlEiOldBZGRkZGRkZA=="
    dec = decode(TEST)
    enc = encode(dec)
    print(dec)
    print(enc)
    print(TEST == enc)
