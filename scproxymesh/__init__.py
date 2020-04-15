"""Proxymesh downloader middleware for Scrapy"""
__author__ = 'mizhgun@gmail.com, junta.kristobal@gmail.com'
# Py3k conversion by: junta.kristobal@gmail.com

import base64
import itertools

try:
    from urllib2 import _parse_proxy
except ImportError:
    from urllib.request import _parse_proxy

from scrapy import Request, Spider
from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings
from scrapy.utils.misc import arg_to_iter
from six.moves.urllib.parse import unquote, urlunparse


class SimpleProxymeshMiddleware:
    """Proxymesh downloader middleware for Scrapy"""

    def __init__(self, settings: Settings):
        """
        :param scrapy.settings.Settings settings:
        """
        if not settings.getbool('PROXYMESH_ENABLED', True):
            raise NotConfigured
        self.proxies = itertools.cycle(arg_to_iter(settings.get('PROXYMESH_URL', 'http://us-il.proxymesh.com:31280')))
        self.timeout = settings.getint('PROXYMESH_TIMEOUT', 0)

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        return o

    @staticmethod
    def _get_proxy(url: str) -> (str, str):
        """
        Transform proxy url into a tuple of credentials and proxy url without credentials

        :param str url:
        :return str, str: credentials, proxy url
        """
        proxy_type, user, password, hostport = _parse_proxy(url)
        proxy_url = urlunparse((proxy_type, hostport, '', '', '', ''))

        if user and password:
            user_pass = '%s:%s' % (unquote(user), unquote(password))
            creds = base64.b64encode(user_pass.encode("utf-8")).strip()
        else:
            creds = None

        return creds, proxy_url

    def process_request(self, request: Request, spider: Spider) -> None:
        """
        Add proxy to the request

        :param scrapy.Request request:
        :param scrapy.Spider spider:
        :return None:
        """
        if not request.meta.get('bypass_proxy', False) and request.meta.get('proxy') is None:
            creds, proxy = self._get_proxy(next(self.proxies))
            request.meta['proxy'] = proxy
            if creds:
                request.headers['Proxy-Authorization'] = b'Basic ' + creds
            if self.timeout and not request.headers.get('X-ProxyMesh-Timeout'):
                request.headers.update({'X-ProxyMesh-Timeout': self.timeout})
