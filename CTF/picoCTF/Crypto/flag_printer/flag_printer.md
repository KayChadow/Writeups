
# flag_printer - NOT SOLVED - TOO HARD

*Hard*

>### Description
>I made a program to solve a problem, but it seems too slow :(\
>Download the program [here](./flag_printer.py).\
>Download the message [here](./encoded.txt).

## Solution

### Recon

This is the program:
```python
import galois
import numpy as np
MOD = 7514777789

points = []

for line in open('encoded.txt', 'r').read().strip().split('\n'):
    x, y = line.split(' ')
    points.append((int(x), int(y)))

GF = galois.GF(MOD)

matrix = []
solution = []
for point in points:
    x, y = point
    solution.append(GF(y % MOD))

    row = []
    for i in range(len(points)):
        row.append(GF((x ** i) % MOD))

    matrix.append(GF(row))

open('output.bmp', 'wb').write(bytearray(np.linalg.solve(GF(matrix), GF(solution)).tolist()[:-1]))
```

And the encoded file is a very large file that looks like this:
```
0 66
1 77611334
2 7296865972
3 6005985327
4 2768154539
5 3553732454
6 1992438015
7 538931207
8 3393488850
9 1014238907
10 5980514119
11 928281187
12 3328481670
13 2083418691
14 4530729570
15 1519132131
16 4341836794
...
1769608 5804619098
1769609 490663452
1769610 2894722434
```

I added a simple print statement `print(f"[*] Point: {point}")` to see how slow it was going. And well, it was quite slow. 

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{}
</details>