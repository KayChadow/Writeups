
# SideChannel

*Hard*

>### Description
>There's something fishy about this PIN-code checker, can you figure out the PIN and get the flag?
>Download the PIN checker program here [pin_checker]()\
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


<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{}
</details>