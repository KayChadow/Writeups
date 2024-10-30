
# Programming a language

*Medium*

>### Description
>My friend is a total "programming languages freak", to the point, that he's decided to make one himself!
>
>The language works like that:
>
> Language is based on stack (works somewhat like an array)\
> Initially stack consists of one element, which value is 0
>
> "-" decreases stack's last element's value by 1\
> "+" increases stack's last element's value by 1\
> ">" puts first element at the end of the stack and shifts every other down\
> "<" puts last element at the beginning of the stack and shifts every other up\
> "@" exchanges last 2 elements\
> "." duplicates stack's last element and puts it at the end of the stack\
> "€" prints out every stack's element's value in ASCII (from the first to the last element)
>
>Example #1: ".+.-->.<@" (char | stack):
>
> Init | [0]\
> "."  | [0, 0]\
> "+"  | [0, 1]\
> "."  | [0, 1, 1]\
> "-"  | [0, 1, 0]\
> "-"  | [0, 1, -1]\
> ">"  | [1, -1, 0]\
> "."  | [1, -1, 0, 0]\
> "<"  | [0, 1, -1, 0]\
> "@"  | [0, 1, 0, -1]\
>
>Example #2:
>
> Let's suppose we have a stack like this: [97, 98, 99]\
> Then, if there is "€" at this point, the output would be: "abc"\
>Based on that info, could you give me the output of your input ([file](./input.txt) attached)?

## Solution

### Recon

The programming language kinda looks like brainfuck, except it is simpler and with no loops. 

This is the input file:
```
++++++++++++++++++++++++++++++++++++++++++++++++.++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.++.----------->@>>.<@<<<.@<@<@<++++<.<@<@<<@<-----.<<<<<.<@<@<+<.+>@.-------.-------->>>.<@<@<++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.++>>>.<@<@<<.-----------<.>@>@<@><<.>@>@++++<.>@-----.>>>.<@<@<+<.>@+.-------.--------.+++++++++++++>>>>>>.<@<@<@<@<@<<.>@++.-------<.>@+++++++<<<.>@>@>@<<.>@>@<.>@-<.>@++++++++++++<<<.>@>@>@+++++++++++€
```

If it were smaller, it could have been done by hand. But luckily, it is really straightforward to implement in python.

### Exploit

This is how I implemented every function:

```python
def min(stack):
        stack[-1] -= 1

def plus(stack):
        stack[-1] += 1

def right(stack):
        stack.append(stack.pop(0))

def left(stack):
        stack.insert(0,stack.pop())

def at(stack):
        stack[-1],stack[-2] = stack[-2],stack[-1]

def dot(stack):
        stack.append(stack[-1])

def euro(stack):
        print(*[chr(c) for c in stack], sep='')
```

Simply add some if statements to run it over every character in the input file.

Full code [here](./exploit.py).

<details>
<summary>Yes! We got the flag:</summary> 
CTFlearn{pr0gr4mm1ng_pr0gr4mm1ng_l4ngu4g3s?}
</details>