
# Picker I

*Medium*

>### Description
>This service can provide you with a random number, but can it do anything else?
Connect to the program with netcat:
>```sh
>nc saturn.picoctf.net 59503
>```
>The program's source code can be downloaded [here](https://artifacts.picoctf.net/c/514/picker-I.py).

### Solution

The source code file contains a lot of bullshit, useless code, big comments.
In the source code we find the main loop of the program:

```python
while(True):
  try:
    print('Try entering "getRandomNumber" without the double quotes...')
    user_input = input('==> ')
    eval(user_input + '()')
  except Exception as e:
    print(e)
    break
```

This basically allows us to call any function that is already defined. Luckily for us, there is this interesting function that kinda prints the flag:

```python
def win():
  # This line will not work locally unless you create your own 'flag.txt' in
  #   the same directory as this script
  flag = open('flag.txt', 'r').read()
  #flag = flag[:-1]
  flag = flag.strip()
  str_flag = ''
  for c in flag:
    str_flag += str(hex(ord(c))) + ' '
  print(str_flag)
```

We can call this by just entering 'win' as our input to the netcat server. This prints a hex encoded version of the flag:

>0x70 0x69 0x63 0x6f 0x43 0x54 0x46 0x7b 0x34 0x5f 0x64 0x31 0x34 0x6d 0x30 0x6e 0x64 0x5f 0x31 0x6e 0x5f 0x37 0x68 0x33 0x5f 0x72 0x30 0x75 0x67 0x68 0x5f 0x36 0x65 0x30 0x34 0x34 0x34 0x30 0x64 0x7d

Just simply decode this.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{4_d14m0nd_1n_7h3_r0ugh_6e04440d}
</details>