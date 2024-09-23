# DOMDOM Patriot CTF 2024
@phulelouch
### Problem:
```
@app.route('/check', methods=['POST', 'GET'])
def check():
    r = requests.Session()
    allow_ip = request.headers['Host']
    if request.method == 'POST':
        url = request.form['url']
        url_parsed = urllib.parse.urlparse(url).netloc 
        if allow_ip == url_parsed:
            get_content = r.get(url = url)
        else:
            return "Cannot request for that url"
        try:
            parsed_json = json.loads(get_content.content.decode())["Comment"]
            parser = etree.XMLParser(no_network=False, resolve_entities=True)
            get_doc = etree.fromstring(str(parsed_json), parser)
            print(get_doc, "ho")
            result = etree.tostring(get_doc)
        except:
            return "Something wrong!!"
        if result: return result
        else: return "Empty head"
    else:
        return render_template('check.html') 
```

```
image = Image.open(name)
            image_dict = {
                   "Filename": image.filename,
                   "Image Size": image.size,
                   "Comment": image.info.get('Comment')
                   }
            return image_dict
```

### Way of thinking :
The problem is a web application that allows users to upload images and then parse the image's EXIF data. The application uses the `Pillow` library to open the image and extract the EXIF. Then load into  a dictionary and return it. The problem is that the application does not validate the image's EXIF and load it into XML  

TL;DR: This `"Comment": image.info.get('Comment')` and this
```
parsed_json = json.loads(get_content.content.decode())["Comment"]
parser = etree.XMLParser(no_network=False, resolve_entities=True)
get_doc = etree.fromstring(str(parsed_json), parser)
```
are the key to the problem. The application is vulnerable to XXE (XML External Entity) attacks

###  Solution:

I use ChatGPT to write the code create an image and replace the comment with a malicious XML payload that read /app/flag.txt. Then just /check it

The code is in domdom_exploit.py

![alt text](<Screenshot 2024-09-22 at 3.36.09 PM.png>)
