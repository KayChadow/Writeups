
# Transposion-trail

*Medium*

>### Description
>Our data got corrupted on the way here. Luckily, nothing got replaced, but every block of 3 got scrambled around! The first word seems to be three letters long, maybe you can use that to recover the rest of the message.
>Download the corrupted message [here](https://artifacts.picoctf.net/c/193/message.txt).

### Solution

This is the content of the file, the scrambled flag:

>heTfl g as iicpCTo{7F4NRP051N5_16_35P3X51N3_V9AAB1F8}7

The description makes me believe we have to do the same thing with each block of 3 characters. It seems like the file content will spell out something like "The flag is picoCTF{}". This corresponds with unscrambling each block of characters 'abc' to 'cab'. Lets try this for the whole file to uncover the flag.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{7R4N5P051N6_15_3XP3N51V3_A9AFB178}
</details>