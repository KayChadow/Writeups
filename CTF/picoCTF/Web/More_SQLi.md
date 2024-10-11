
# More SQLi

*Medium*

>### Description
>Can you find the flag on this website.
>Try to find the flag [here](http://saturn.picoctf.net:57651/).

### Solution

We are greeted with a login screen. When we fill in foo:bar, we can see the executed query by the server:

>SQL query: SELECT id FROM users WHERE password = 'bar' AND username = 'foo'

We can try logging in by performing SQL injection on the password field with the following payload:
```SQL
' OR 1=1 -- 
```
This allows us to log in, and in the response we can see the flag.

<details>
<summary>Yes! We got the flag:</summary> 
picoCTF{G3tting_5QL_1nJ3c7I0N_l1k3_y0u_sh0ulD_c8ee9477}
</details>