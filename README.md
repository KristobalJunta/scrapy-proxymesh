# scrapy-proxymesh-py3

Proxymesh downloader middleware for Scrapy.

This is a fork of [scrapy-proxymesh](https://github.com/mizhgun/scrapy-proxymesh) that supports Python 3.

This package replaces the original, as it ships under the same name (scproxymesh).

## Installation

### From PyPI

```
pip install scrapy-proxymesh-py3
```

### From GitHub

```
pip install -e git+https://github.com/KristobalJunta/scrapy-proxymesh@master#egg=scproxymesh
```

## Usage

- Register free acount from https://www.proxymesh.com/
- Add the following to settings.py:

```python
DOWNLOADER_MIDDLEWARES = {
    'scproxymesh.SimpleProxymeshMiddleware': 100,
}

# if you use user & password auth
PROXYMESH_URL = 'http://username:password@us-il.proxymesh.com:31280'

# or, if you use ip-based auth:
PROXYMESH_URL = 'http://us-il.proxymesh.com:31280'

# Proxymesh request timeout
PROXYMESH_TIMEOUT = 60
```
