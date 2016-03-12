from urllib.parse import urljoin
import requests

from restservice import exceptions


class Endpoint(object):

    def __init__(self, service, method_name, path):
        self.method = self._get_method(method_name)
        self.path = path
        self.service = service

    def _get_method(self, method_name):
        try:
            return getattr(requests, method_name.lower())
        except AttributeError:
            raise exceptions.ServiceException(
                '{} is not supported'.format(method_name)
            )

    def _build_url(self):
        return urljoin(self.service.url, self.path)

    def call(self, params=None, payload=None, headers=None, silent_fail=False):
        response = self.method(
            url=self._build_url(),
            params=params,
            json=payload,
            headers=headers,
        )
        if not silent_fail:
            response.raise_for_status()
        return response.json()


class Service(object):

    _endpoints = {}

    def __init__(self, url):
        self.url = url

    def add(self, name, method_name, path):
        self._endpoints[name] = Endpoint(self, method_name, path)

    def __getattr__(self, attr):
        try:
            return self._endpoints[attr]
        except KeyError:
            raise AttributeError('No such endpoint as \'{}\''.format(attr))
