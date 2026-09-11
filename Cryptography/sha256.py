# Manually implementing the exactingly specific hashing algorithm SHA-256

# Debug functions
def toBinary(val: int, n: int):
    res = ""
    for x in range(n-1, -1, -1):
        res += str(val >> x & 1)
        if x % 8 == 0:
            res += " "
    return res

def printW(w: list[int]):
    for i in range(0, len(w), 2):
        print(toBinary(w[i], 32), toBinary(w[i+1], 32))

# Constants
# k = ['01000010100010100010111110011000', '01110001001101110100010010010001', '10110101110000001111101111001111', '11101001101101011101101110100101', '00111001010101101100001001011011', '01011001111100010001000111110001', '10010010001111111000001010100100', '10101011000111000101111011010101', '11011000000001111010101010011000', '00010010100000110101101100000001', '00100100001100011000010110111110', '01010101000011000111110111000011', '01110010101111100101110101110100', '10000000110111101011000111111110', '10011011110111000000011010100111', '11000001100110111111000101110100', '11100100100110110110100111000001', '11101111101111100100011110000110', '00001111110000011001110111000110', '00100100000011001010000111001100', '00101101111010010010110001101111', '01001010011101001000010010101010', '01011100101100001010100111011100', '01110110111110011000100011011010', '10011000001111100101000101010010', '10101000001100011100011001101101', '10110000000000110010011111001000', '10111111010110010111111111000111', '11000110111000000000101111110011', '11010101101001111001000101000111', '00000110110010100110001101010001', '00010100001010010010100101100111', '00100111101101110000101010000101', '00101110000110110010000100111000', '01001101001011000110110111111100', '01010011001110000000110100010011', '01100101000010100111001101010100', '01110110011010100000101010111011', '10000001110000101100100100101110', '10010010011100100010110010000101', '10100010101111111110100010100001', '10101000000110100110011001001011', '11000010010010111000101101110000', '11000111011011000101000110100011', '11010001100100101110100000011001', '11010110100110010000011000100100', '11110100000011100011010110000101', '00010000011010101010000001110000', '00011001101001001100000100010110', '00011110001101110110110000001000', '00100111010010000111011101001100', '00110100101100001011110010110101', '00111001000111000000110010110011', '01001110110110001010101001001010', '01011011100111001100101001001111', '01101000001011100110111111110011', '01110100100011111000001011101110', '01111000101001010110001101101111', '10000100110010000111100000010100', '10001100110001110000001000001000', '10010000101111101111111111111010', '10100100010100000110110011101011', '10111110111110011010001111110111', '11000110011100010111100011110010']
k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

def sha256(message: str):
    if len(message) >= 1 << 62:
        raise ValueError("Message above size limit")
    
    # Hash values
    # h = ['01101010000010011110011001100111', '10111011011001111010111010000101', '00111100011011101111001101110010', '10100101010011111111010100111010', '01010001000011100101001001111111', '10011011000001010110100010001100', '00011111100000111101100110101011', '01011011111000001100110100011001']
    h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
    
    # Translate the string into 512-bit chunks, stored as a list of integers
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
    
    # Add the 0x80 byte at the end, and add 0 bits as padding to ensure all chunks are whole
    # Append length of message (in bits) using 64 bits
    if n < 56:
        acc = ((acc << 8) + 0x80 << (63 - n) * 8) + len(message) * 8
    else:
        chunks.append((acc << 8) + 0x80 << (63 - n) * 8)
        acc = len(message) * 8
    chunks.append(acc)
    
    # Mutate hash values per chunk
    for chunk in chunks:
        # Extract the chunk and split it into 32-bit words, to form the message schedule
        w = []
        for i in range(480, -1, -32):
            w.append(chunk >> i & 0xffffffff)
        
        # Expand message schedule using bitwise operations
        for _ in range(48):
            s0 = rotate_right(w[-15], 7) ^ rotate_right(w[-15], 18) ^ w[-15] >> 3
            s1 = rotate_right(w[-2], 17) ^ rotate_right(w[-2], 19) ^ w[-2] >> 10
            w.append((s0 + s1 + w[-16] + w[-7]) % (1 << 32))

        # Perform compression by using the message schedule to mutate copies of the hash values, iterating 64 times
        v = h[:]
        for j in range(64):
            # Choice function
            ch = v[4] & v[5] ^ ~v[4] & v[6]
            # Majority function
            maj = v[0] & v[1] ^ v[0] & v[2] ^ v[1] & v[2]
            t = (v[7] + ch + k[j] + w[j] + (rotate_right(v[4], 6) ^ rotate_right(v[4], 11) ^ rotate_right(v[4], 25))) % (1 << 32)
            for m in range(7, 0, -1):
                v[m] = v[m-1]
            v[0] = (t + maj + (rotate_right(v[0], 2) ^ rotate_right(v[0], 13) ^ rotate_right(v[0], 22))) % (1 << 32)
            v[4] = (v[4] + t) % (1 << 32)
        
        # Update hash values for current message using addition
        for l in range(8):
            h[l] = (h[l] + v[l]) % (1 << 32)
    
    # Convert each hash value to a string, then concatenate to form digest
    return "".join(f"{h[p]:08x}" for p in range(8))

# ROR word by n bits. n CANNOT be negative. word is assumed to be 32 bits long.
def rotate_right(word: int, n: int):
    if n < 0:
        raise ValueError("n is negative")
    
    return ((word & (1 << n) - 1) << 32 - n) | (word >> n)

if __name__ == "__main__":
    import hashlib

    TEST = "Test message blah blah !@(!)ddddddddddddddddddddddddddddddddddd"
    # TEST = "Test message blah blah !@(!)"
    # TEST = "Hello, World!"
    # TEST = "hello world"
    # TEST = "Quartron's Eye shall rise to dominate the world!!!! AHAHAHHAA"
    print(len(TEST))
    res = sha256(TEST)
    print(res)
    lib = hashlib.sha256(TEST.encode("utf-8")).hexdigest()
    print(lib)
    print(res == lib)