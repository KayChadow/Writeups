
# SideChannel

*Hard*

>### Description
>There's something fishy about this PIN-code checker, can you figure out the PIN and get the flag?
>Download the PIN checker program here [pin_checker](./pin_checker)\
>Once you've figured out the PIN (and gotten the checker program to accept it), connect to the master server using `nc saturn.picoctf.net 57350` and provide it the PIN to get your flag.

## Solution

### Recon

The program asks for our 8 digit PIN code: *"Please enter your 8-digit PIN code:"* When we enter some code like "12345678" it prints the length "8", and then says *"Checking PIN... Access denied."*

The first hint lets us know that we have to use "timing-based side-channel attacks". It means that the program can have different execution times based on the correctness of the inputted PIN code. 

### Exploit

So to time the execution of the program I use this command:

```bash
time echo "00000000" | ./pin_checker
```

This took about 0.1 second:

```
Please enter your 8-digit PIN code:
8
Checking PIN...
Access denied.

real    0m0.135s
user    0m0.135s
sys     0m0.000s
```

Now I manually change the leftmost digits to all numbers 0 to 9. 

Notice when I run `time echo "40000000" | ./pin_checker`, it suddenly takes about 0.11 second longer than normal. This probably means that 4 is the correct digit, and that the program was also checking the second digit for correctness.

Brute force this digit by digit. When execution takes more than 0.1 second longer, it is the right digit.

Eventually I find this PIN: "48390513". Now fill this in on the server.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{t1m1ng_4tt4ck_914c5ec3}
</details>