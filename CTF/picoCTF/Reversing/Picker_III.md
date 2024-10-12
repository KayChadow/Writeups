
# Picker III

*Medium*

>### Description
>Can you figure out how this program works to get the flag?
>Connect to the program with netcat:
>```
>nc saturn.picoctf.net 61221
>```
>The program's source code can be downloaded [here](https://artifacts.picoctf.net/c/525/picker-III.py).

### Solution

We can see a little menu where we can input a number from 1 to 4 to execute that function. Function number 3 is 'write_variable'. This seems quite interesting. Lets look at the source code of this method:

```python
def filter_var_name(var_name):
  r = re.search('^[a-zA-Z_][a-zA-Z_0-9]*$', var_name)
  if r:
    return True
  else:
    return False

def filter_value(value):
  if ';' in value or '(' in value or ')' in value:
    return False
  else:
    return True

def write_variable():
  var_name = input('Please enter variable name to write: ')
  if( filter_var_name(var_name) ):
    value = input('Please enter new value of variable: ')
    if( filter_value(value) ):
      exec('global '+var_name+'; '+var_name+' = '+value)
    else:
      print('Illegal value')
  else:
    print('Illegal variable name')
```

In the code there exists a function 'win()' that prints the flag in hex.
We want to change the functions we can call, so we can call 'win()' to print the flag. The variable 'func_table' stores the allowed functions in a string:

```
print_table                     read_variable                   write_variable                  getRandomNumber                 
```

Every function is padded with spaces to 32 characters. This is also checked frequently in the program. We want to have the ability to call 'win' instead of 'getRandomNumber'. So replace 'getRandomNumber' with 'win' appended with 12 spaces. 

Surround with "" for the payload to set the variable 'func_table' to the payload string:

```
"print_table                     read_variable                   write_variable                  win                             "
```

Use options 3 to write the variable 'func_table' with the given payload.
Now we can call the 'win()' function. This prints the flag in hex. Just simply decode.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{7h15_15_wh47_w3_g37_w17h_u53r5_1n_ch4rg3_a186f9ac}
</details>