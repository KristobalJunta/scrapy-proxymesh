# -*- coding: utf-8 -*-
from base64 import b64encode

import pytest
import scrapy
from scrapy.settings import Settings
from scproxymesh import SimpleProxymeshMiddleware


class TestSimpleProxymeshMiddleware:
    alt_proxy = "http://spam:eggs@example.com"
    user = "user"
    password = "password"
    url = "example.org"
    port = 1234
    timeout = 42

    @pytest.fixture
    def settings(self):
        return Settings({
            "PROXYMESH_ENABLED": True,
            "PROXYMESH_URL": f"http://{self.user}:{self.password}@{self.url}:{self.port}",
            "PROXYMESH_TIMEOUT": 0,
        })

    def test_get_proxy(self, settings):
        m = SimpleProxymeshMiddleware(settings)
        url = settings.get("PROXYMESH_URL")
        creds, proxy_url = m._get_proxy(url)

        assert creds == b64encode(f"{self.user}:{self.password}".encode())
        assert proxy_url == f"http://{self.url}:{self.port}"

    def test_process_request(self, settings):
        request = scrapy.Request("http://example.org", meta={})
        m = SimpleProxymeshMiddleware(settings)
        m.process_request(request, None)

        assert "proxy" in request.meta

    def test_process_request_with_timeout(self, settings):
        settings.set("PROXYMESH_TIMEOUT", self.timeout)
        request = scrapy.Request("http://example.org", meta={})
        m = SimpleProxymeshMiddleware(settings)
        m.process_request(request, None)

        assert "X-ProxyMesh-Timeout" in request.headers
        assert request.headers["X-ProxyMesh-Timeout"] == str(self.timeout).encode()

    def test_process_request_with_proxy(self, settings):
        request = scrapy.Request("http://example.org", meta={"proxy": self.alt_proxy})
        m = SimpleProxymeshMiddleware(settings)
        m.process_request(request, None)

        assert request.meta["proxy"] == self.alt_proxy
