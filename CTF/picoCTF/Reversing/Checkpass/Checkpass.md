
# Checkpass

*Hard*

>### Description
>What is the password? File: [checkpass](./checkpass) Flag format: picoCTF{...}

## Solution

### Recon

Run the binary:
```
Usage:
        ./checkpass <password>
```

When I try to run `./checkpass a`, I get an error message saying "Invalid length". So I imagine that there are different error messages that allow me to get to the password.

### Exploit

So I repeatedly add an 'a' to the password to find the length.

The password length appears to be 41 characters.
```bash
./checkpass aaaabbbbccccddddeeeeffffgggghhhhiiiijjjjk
```
This prints "Invalid password".

>---
>So apparently this is entirely wrong, you have to decompile the rust file, and get the password that way...
>---

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{}
</details>