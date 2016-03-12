import unittest
import requests
import json
from mock import patch

from pyservice.builder import Service, Endpoint
from pyservice.exceptions import ServiceException


class ServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.service = Service('http://test')

    def test_add(self):
        self.service.add('api', 'post', '/api')
        self.assertIsInstance(self.service.api, Endpoint)

    def test_non_existing_endpoint(self):
        with self.assertRaises(AttributeError) as cm:
            self.service.non_existing

        self.assertEqual(
            str(cm.exception), 'No such endpoint as \'non_existing\''
        )


class EndpointTestCase(unittest.TestCase):

    def setUp(self):
        self.service = Service('http://test')

        patcher = patch('requests.api.request')
        self.addCleanup(patcher.stop)
        self.mock_request = patcher.start()

    def test_get_method(self):
        endpoint = Endpoint(self.service, 'post', '/path')
        self.assertEqual(requests.post, endpoint.method)

        endpoint = Endpoint(self.service, 'get', '/path')
        self.assertEqual(requests.get, endpoint.method)

        endpoint = Endpoint(self.service, 'put', '/path')
        self.assertEqual(requests.put, endpoint.method)

    def test_get_non_existing_method(self):
        with self.assertRaises(ServiceException) as cm:
            Endpoint(self.service, 'non_existing', '/path')

        self.assertEqual(
            str(cm.exception), 'non_existing is not supported'
        )

    def test_build_url(self):
        self.assertEqual(
            Endpoint(self.service, 'post', '/path')._build_url(),
            'http://test/path'
        )

    def test_call(self):
        resp_data = {'test': 'ok'}
        resp = requests.Response()
        resp.status_code = 200
        resp._content = bytes(json.dumps(resp_data), 'utf-8')
        self.mock_request.return_value = resp
        endpoint = Endpoint(self.service, 'post', '/path')
        self.assertEquals(endpoint.call(), resp_data)
