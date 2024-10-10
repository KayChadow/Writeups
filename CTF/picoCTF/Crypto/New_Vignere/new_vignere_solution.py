import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

print(f"Alphabet is: {ALPHABET}")

enc_flag = "bkglibgkhghkijphhhejggikgjkbhefgpienefjdioghhchffhmmhhbjgclpjfkp"

def b16_encode(plain):
        enc = ""
        for c in plain:
                binary = "{0:08b}".format(ord(c))
                enc += ALPHABET[int(binary[:4], 2)]
                enc += ALPHABET[int(binary[4:], 2)]
        return enc

def b16_decode(cipher):
        plain = ""
        for i in range(0, len(cipher)-1, 2):
                binary = "{0:04b}".format(ALPHABET.find(cipher[i])) + "{0:04b}".format(ALPHABET.find(cipher[i+1]))
                plain += chr(int(binary, 2))
        return plain

def shift(c, k):
        t1 = ord(c) - LOWERCASE_OFFSET
        t2 = ord(k) - LOWERCASE_OFFSET
        return ALPHABET[(t1 + t2) % len(ALPHABET)]

def shift_reverse(enc, k):
        t2 = ord(k) - LOWERCASE_OFFSET
        t1 = ALPHABET.find(enc) - t2
        if t1 < 0:
                t1 += len(ALPHABET)
        return chr(t1 + LOWERCASE_OFFSET)

# flag = "redacted"
# assert all([c in "abcdef0123456789" for c in flag])
#
# key = "redacted"
# assert all([k in ALPHABET for k in key]) and len(key) < 15
#
# b16 = b16_encode(flag)
# enc = ""
# for i, c in enumerate(b16):
#       enc += shift(c, key[i % len(key)])
# print(enc)

def decode(enc, key):
        b16 = ""
        for i, c in enumerate(enc):
                b16 += shift_reverse(c, key[i % len(key)])
        plain = b16_decode(b16)
        return plain

def get_key_size2(num):
        return ALPHABET[num%16] + ALPHABET[num//16]

# brute force loop to find possible pairs of key characters
for i in range(0, len(enc_flag)-1, 2):
        enc_part = enc_flag[i:i+2]
        print(f"Breaking part {i}: {enc_part}")
        for j in range(256):
                key = get_key_size2(j)
                plain_maybe = decode(enc_part, key)
                if all([c in "abcdef0123456789" for c in plain_maybe]):
                        print(key)

# This is the manually found key
manually_found_key = "oedcfjdbe"
print(f"This is decoded with {manually_found_key}: {decode(enc_flag, manually_found_key)}")