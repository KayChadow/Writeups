
# babygame01

*Medium*

>### Description
>Get the flag and reach the exit.\
>Welcome to BabyGame! Navigate around the map and see what you can find! The game is available to download [here](https://artifacts.picoctf.net/c/222/game). There is no source available, so you'll have to figure your way around the map. You can connect with it using:
>```
>nc saturn.picoctf.net 55876
>```

### Solution

We don't have source code, but we do have a binary. So the first thing to do in decompile the binary using Ghidra. This is the main method:

```c
undefined4 main(void)

{
  int iVar1;
  undefined4 uVar2;
  int in_GS_OFFSET;
  int local_aac;
  int local_aa8;
  char local_aa4;
  undefined local_aa0 [2700];
  int local_14;
  undefined *local_10;
  
  local_10 = &stack0x00000004;
  local_14 = *(int *)(in_GS_OFFSET + 0x14);
  init_player(&local_aac);
  init_map(local_aa0,&local_aac);
  print_map(local_aa0,&local_aac);
  signal(2,sigint_handler);
  do {
    do {
      iVar1 = getchar();
      move_player(&local_aac,(int)(char)iVar1,local_aa0);
      print_map(local_aa0,&local_aac);
    } while (local_aac != 0x1d);
  } while (local_aa8 != 0x59);
  puts("You win!");
  if (local_aa4 != '\0') {
    puts("flage");
    win();
    fflush(_stdout);
  }
  uVar2 = 0;
  if (local_14 != *(int *)(in_GS_OFFSET + 0x14)) {
    uVar2 = __stack_chk_fail_local();
  }
  return uVar2;
}
```

To get the flag we must execute the `win()` function. 

User input to move the user position gets parsed in the `move_player()` function:

```c
void move_player(int *param_1,char param_2,int param_3)

{
  int iVar1;
  
  if (param_2 == 'l') {
    iVar1 = getchar();
    player_tile = (undefined)iVar1;
  }
  if (param_2 == 'p') {
    solve_round(param_3,param_1);
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
  *(undefined *)(*param_1 * 0x5a + param_3 + param_1[1]) = player_tile;
  return;
}
```
There are normal move options: w,a,s,d. And 'p' to go to the end immediately, and 'l' to change the player_tile.

> I was confused and used [this](https://github.com/snwau/picoCTF-2023-Writeup/blob/main/Binary%20Exploitation/babygame01/babygame01.md) writeup to help myself out.

We can see that it is not checked if the player goes out of bounds of the map array, and it just writes the player_tile to that memory address. This allows us to write anything anywhere by moving to the location and using 'l'+'anything' to write that anything there. 

From the `main()` we notice that the important variable `local_aa4` is right below the map on the stack:
```c
...
  char local_aa4;
  undefined local_aa0 [2700];
...
```

The check for the flag `if (local_aa4 != '\0')` only checks one character of the 4 byte variable (thereby only the lsb). Since it is little endian, we have to move 4 spaces before the beginning of the map to overwite the lsb of local_aa4. 

So to exploit, move to (0 -4) while having a player_tile that is not \x00 (standard). And then press 'p' to get the flag.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{gamer_m0d3_enabled_ec1f4e25}
</details>