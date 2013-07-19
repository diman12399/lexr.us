# lexr.us

An open source URL shortener built with love
using [TornadoWeb](http://www.tornadoweb.org) / [Redis](http://redis.io/) / [PureCSS](http://purecss.io/) / [ZeptoJS](http://zeptojs.com).

![Screenshot](https://f.cloud.github.com/assets/219689/824974/8d41befa-f057-11e2-8ebc-8129357da309.png)


### Live Demo

[lexr.us](http://lexr.us) is running on my Mac Mini Server hosted at MacMiniVault.com


### Features

* iOS 7-style, sleek and elegant interface ☜(ˆ▽ˆ)
* Support all protocols not only http|https
* Bleeding-edge performance


### Requirements

* A Unix server
* Python 2.7+
* Redis database
* Nginx is optional


### Running the server

* Install the Python dependencies: ```pip install --ignore-installed -r requirements.txt```
* Install Redis: ```brew install redis``` if Mac_with_Homebrew else ```xyz install redis```
* Start the server: ```python app.py --logging=none --host=localhost --port=8899```

#### Supervisor config example

```
[program:lexr_us]
command=/usr/local/bin/python app.py --logging=none
directory=/var/www/lexr.us/
autostart=true
autorestart=true
```

#### Nginx config example

```
upstream lexrus {
    server localhost:1983;
}

server {
    listen       80;
    server_name  lexr.us www.lexr.us;

    location / {
        proxy_buffers 8 16k;
        proxy_buffer_size 32k;

        proxy_read_timeout 50s;

        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://lexrus;
        break;
    }
}
```

### API

```
curl -X POST -d "text_mode=1&url=http://www.apple.com/" http://lexr.us/api/url
```

outputs:

```
http://lexr.us/A
```


### LICENSE

Copyright (C) 2013 LexTang.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.