
# c0rrupt

*Medium*

>### Description
>We found [this](https://jupiter.challenges.picoctf.org/static/ab30fcb7d47364b4190a7d3d40edb551/mystery) file. Recover the flag.

### Solution

The file is a mystery. Exiftool gives an error when trying to get the file type:

>Error                           : Unknown file type

The hint says we have to fix the file header. The best matching file header I could find [here](https://en.wikipedia.org/wiki/List_of_file_signatures) is PNG, and this is the header:

```
89 50 4E 47 0D 0A 1A 0A
```

Trying to display the file doesn't give an error now, but it still does not display any image. 

I was kinda stuck, and had to use a [writeup](https://medium.com/@mohammedsbihi11/picoctf-c0rrupt-walkthrough-9b40ac5b1ccc) as a guide. This also got me to install the 'pngcheck' tool to work with.

PNG chunks consist of: length (4 bytes), type (4 bytes), data, CRC (4 bytes). The first chunk is the 'IHDR' header, so lets fix this header. We only have to change the type to 'IHDR' in hex, and the CRC is already good.

Now with 'pngcheck' we find that the CRC of the 'pHYs' chunk is incorrect. So fix it with the value that pngcheck gives us. If I run pngcheck again, I find it weird that it says this:

>chunk pHYs at offset 0x00042, length 9: 2852132389x5669 pixels/meter

So I change the first number to be the same a the second so our image has same resolution in x and y direction. But now the CRC is wrong again, and apperently it was correct all along, so I change it back to what is was.

Pngcheck now says "invalid chuck length (too large)" (it is 0xAAAAFFA5) after the 'pHYs' chunk. This next chunk has size "AA AA FF A5" and type "ab D E T", which is not any correct type. The closest type is "IDAT", so lets change it to "IDAT"... Still the chuck is too big. The IDAT chunk contains the image data, so I imagine the next chunks is also going to be an IDAT chunk. With this command I find out where other IDAT chunks are:

```bash
binwalk -R "IDAT" mystery
```

The next "IDAT" is at 0x10008, so the next chunk is at 0x10008 - 0x4 = 0x10004. The end of the first IDAT chunk also contains a 4 byte CRC, so the length of the data part is 0x10004 - 0x4 - 0x5B (start address of data part) = 0xFFA5, so change size from 0xAAAAFFA5 to 0x0000FFA5.

Since pngcheck doesn't detect any errors, we can try to open the image.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{c0rrupt10n_1847995}
</details>