
# Substitution1

*Medium*

>### Description
>A second message has come in the mail, and it seems almost identical to the first one. Maybe the same thing will work again.
>Download the message [here](https://artifacts.picoctf.net/c/181/message.txt)

### Solution

This time we don't know the key. But luckily, an alphabetical substitution cipher is quite easy to crack. So just search for a substitution cipher breaker online, and fill in the ciphertext.

Oops! It is not correct. But I find the mistake easily since the (wrong) flag contains "FR3JU3NCY" which obviously has to spell frequency, so the 'j' has to be a 'q' (two of the least used letters in English). 

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{FR3QU3NCY_4774CK5_4R3_C001_4871E6FB}
</details>