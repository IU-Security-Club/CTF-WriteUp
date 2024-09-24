# Impersonate Patriot CTF 2024
@phulelouch
### Problem:

```
server_start_time = datetime.now()
server_start_str = server_start_time.strftime('%Y%m%d%H%M%S')
secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()
app.secret_key = secure_key
```

### Way of thinking :
Flask secert key using server_start_time and they also public that info at /status

So we can create our own flask session.

###  Solution:

 I write a code to compute the Flask secret key and admin UID then use flask-unsign. The code in PatriotCTF_Impersonate_exploit.py

![alt text](<Screenshot 2024-09-21 at 8.32.56 PM.png>)
![alt text](<Screenshot 2024-09-21 at 8.26.15 PM.png>)
