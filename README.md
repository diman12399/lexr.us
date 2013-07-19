# lexr.us

An open source URL shortener built with love
using [TornadoWeb](http://www.tornadoweb.org) / [Redis](http://redis.io/) / [PureCSS](http://purecss.io/) / [ZeptoJS](http://zeptojs.com).

![Screenshot](https://f.cloud.github.com/assets/219689/824974/8d41befa-f057-11e2-8ebc-8129357da309.png)


### Features

* iOS 7-style, sleek and elegant interface ☜(ˆ▽ˆ)
* Support all protocols not only http|https
* Bleeding-edge performance
* Support for deploying as a upstream for Apache or Nginx


### Requirements

* A Unix server
* Python 2.7+
* Redis database


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

### API

```curl -X POST -d "text_mode=1&url=http://www.apple.com/" http://lexr.us/api/url```

outputs:

```http://lexr.us/A```


### LICENSE

Copyright (C) 2013 LexTang.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.