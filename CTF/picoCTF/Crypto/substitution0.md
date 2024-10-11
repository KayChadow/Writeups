
# Substitution0

*Medium*

>### Description
>A message has come in but it seems to be all scrambled. Luckily it seems to have the key at the beginning. Can you crack this substitution cipher?
>Download the message [here](https://artifacts.picoctf.net/c/153/message.txt).

### Solution

It says the message file starts with the key of the substitution cipher. Which is:

> OHNFUMWSVZLXEGCPTAJDYIRKQB

This means all 'a' are encrypted with 'o', 'b' with 'h', 'c' with 'n', etc. It is alphabetical. Now just find any substitution cipher decoder online, fill in the ciphertext and the key, and decode.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{5UB5717U710N_3V0LU710N_03055505}
</details>