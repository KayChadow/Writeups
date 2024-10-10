
# New Vignere

*Hard*

>### Description
>
>Another slight twist on a classic, see if you can recover the flag. (Wrap with picoCTF{}) 
>>bkglibgkhghkijphhhejggikgjkbhefgpienefjdioghhchffhmmhhbjgclpjfkp
>
>[new_vignere.py](https://mercury.picoctf.net/static/aa30610884045b68f73057a1a6d9d68c/new_vignere.py)

### Solution

In the file we find the encryption algorithm in python:
```python
import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

def b16_encode(plain):
        enc = ""
        for c in plain:
                binary = "{0:08b}".format(ord(c))
                enc += ALPHABET[int(binary[:4], 2)]
                enc += ALPHABET[int(binary[4:], 2)]
        return enc

def shift(c, k):
        t1 = ord(c) - LOWERCASE_OFFSET
        t2 = ord(k) - LOWERCASE_OFFSET
        return ALPHABET[(t1 + t2) % len(ALPHABET)]

flag = "redacted"
assert all([c in "abcdef0123456789" for c in flag])

key = "redacted"
assert all([k in ALPHABET for k in key]) and len(key) < 15

b16 = b16_encode(flag)
enc = ""
for i, c in enumerate(b16):
        enc += shift(c, key[i % len(key)])
print(enc)
```

The **b16_encode(plain)** just splits the binary of a character, 00111111, into two smaller parts, 0011 1111, as characters [a-p], dp. This is fairly easy to reverse:

```python
def b16_decode(cipher):
        plain = ""
        for i in range(0, len(cipher)-1, 2):
                binary = "{0:04b}".format(ALPHABET.find(cipher[i])) + "{0:04b}".format(ALPHABET.find(cipher[i+1]))
                plain += chr(int(binary, 2))
        return plain
```

The **shift(c, k)** does a shift based on the key character (k); if k == "a" -> shift 0, "b" -> shift 1, etc. And return with the weird [a-p] format. Lets reverse this:

```python
def shift_reverse(enc, k):
    t2 = ord(k) - LOWERCASE_OFFSET
    t1 = ALPHABET.find(enc) - t2
    if t1 < 0:
        t1 += len(ALPHABET)
    return chr(t1 + LOWERCASE_OFFSET)
```

With these two functions reversed it is quite easy to implement a **decode(enc, key)** function like this:
```python
def decode(enc, key):
    b16 = ""
    for i, c in enumerate(enc):
        b16 += shift_reverse(c, key[i % len(key)])
    plain = b16_decode(b16)
    return plain
```

The problem is that we don't know the key. I guess we need to brute force it, only two key characters next to each other influence one plaintext character, and we know the plaintext is [a-f0-9]. 

When we brute force we get a lot of possibilities... For each two characters next to each other we get 16 possibilities. These are the possibilities for the first two characters of the key:

>ob, oc, od, le, oe, lf, of, lg, og, lh, oh, li, oi, lj, oj, ok

We see that the key must start with either an 'o' or 'l'. I manually try to find patterns in the brute-forced data.

After 'o' comes either: b, c, d, e, f, g, h, i, j. But since the key is repeating, index 9 could be an 'o', and index 10 can only be 'b' or 'e'. Filtering on index 19, we find second character must be and 'e'. Then 'd'. Repeat this (manually) to find all 9 characters.

We find this key: 'oedcfjdbe'. Plug this this key into our decode function with the given encrypted flag, and wrap it in picoCTF{}.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{698987ddce418c11e9aa564229c50fda}
</details>