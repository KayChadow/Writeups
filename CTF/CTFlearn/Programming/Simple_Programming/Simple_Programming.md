
# Simple Programming

*Easy*

>### Description
>Can you help me? I need to know how many lines there are where the number of 0's is a multiple of 3 or the numbers of 1s is a multiple of 2. Please!\
>Here is the file: [data.dat](./data.dat)

## Solution

### Recon

Seems easy enough. The data file contains a lot of lines of binary numbers, it looks like this:
```
0001100000101010100
110101000001111
101100011001110111
0111111010100
1010111111100011
1110011110010110
11100101010110111
10101101011
1111011101001
0001110001
```

### Exploit

Create a simple python program to find the solution:
```python
#!/bin/python3
out=0
with open("./data.dat", 'r') as f:
        for line in f:
                if line.count('0')%3==0 or line.count('1')%2==0:
                        out+=1
print(out)
```

I wasn't really satisfied, so I made this `grep` one-liner using RegEx:

```bash
grep -Ewc '1*(1*01*01*0)*1*|0*(0*10*1)*0*' data.dat
```

<details>
<summary>Yes! We got the flag:</summary> 
CTFlearn{6662}
</details>