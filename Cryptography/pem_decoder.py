# Given a PEM encoded RSA key (with no headers and whitespace removed), return the exponent and modulus contained in the data.
# Iteration works per byte. The bytes starting \x are those without a Unicode character

import b64

# TODO: Make parser v2 that hardcodes Integer orders pursuant to PKCS rather than testing length
"""
Parser spec:
    Input: Bit string
    Output: (Int|None, Int|None)
Should overall return (modulus, exponent) when fed full key.
If current TLV segment contains both modulus and exponent of the key, returns (modulus, exponent).
If it contains exactly one of modulus or exponent, returns (Int, None)
If contains neither, returns (None, None)

This should automatically differentiate between RSA private and public keys, and between PKCS 1 and 8, returning the correct modulus and exponent.
The parser will fail if any of the following are true:
    - The public exponent is larger than 64 bits
    - Either of the modulus or private exponent are not larger than 64 bits
    - There are integers, tagged 0x02, before either of the modulus and/or exponent
    
This function steps in and recurses on Sequences, Octet Strings, and Bit Strings, returns on Integers, and ignores everything else.
Only the first two Integers larger than 64 bits will be returned.
"""
def parse(bstring: bytes, debug=False, depth=0):
    if not bstring:
        return (None, None)
    # Handle the first TLV segment in the bitstring
    
    # Find length of value
    if bstring[1] & 0x80:
        # The byte is the amt of next bytes that denote actual value length (plus 0x80)
        i = 2+(bstring[1] & 0x7f)
        length = int.from_bytes(bstring[2:i])
    else:
        # The byte is the value length
        length = bstring[1]
        i = 2
    
    if len(bstring) < i+length:
        raise ValueError("Invalid tag length")
    
    if debug:
        print(depth*"-", hex(bstring[0]), "|", bstring[1:i], "| len", length, "| i", i)
    
    # Tags are constructed with bits in pattern 00 0 00000
    # First two bits are always 00 to denote Universal (Types defined by ASN.1) since all types we use will be ASN.1-defined.
    # Third bit is 0 if type is Primitive (raw type, like string) or 1 if Constructed (Nested container, like sequence)
    # Last five bits are the type's specific identifier, defined by ASN.1.
    match bstring[0]:
        # SEQUENCE, BIT STRING, OCTET STRING
        case 0x30 | 0x03 | 0x04:
            # Bit strings have a special case where the first byte is always the number of garbage bits at the end, the padding bits that ensure the bit string is byte-aligned.
            # For RSA this should always be 0x00.
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
            
    # a should NEVER be small unless b is None <- Invariant
    c, d = parse(bstring[i+length:], debug, depth)
    if a == None or c != None and a < 1 << 64:
        return (c,d)
    elif b == None:
        return (a,c)
    elif c != None:
        raise ValueError("(Int, Int) needs to merge with nonempty further parse")
    else:
        return (a,b)
   
def parseFile(filepath, debug=False):
    with open(filepath, "r") as file:
        data = b64.decode("".join(row[:-1] for row in file.readlines()[1:-1]))
    return parse(data, debug)


if __name__ == "__main__":
    import os

    n0, e = parseFile(os.getenv("PRIVATE_KEY_FILE"), True)
    n1, d = parseFile(os.getenv("PUBLIC_KEY_FILE"), True)
    
    print(n0, e)
    print(n1, d)
    print(n0 == n1)