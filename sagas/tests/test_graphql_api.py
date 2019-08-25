#!/usr/bin/env python
"""Unit test for api module GraphQL queries."""
import requests
import unittest

class TestGraphQlApi(unittest.TestCase):
    """Class to execute unit tests for api.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.base_url = 'http://127.0.0.1:5000/graphql'
        self.headers = {'content-type': 'application/json'}

    @classmethod
    def tearDownClass(self):
        """Tear down function called when class is deconstructed."""
        pass

    def test_query_people(self):
        # Get batch list
        payload = '{"query": "{people(id:\\"UGVvcGxlOjE=\\"){name}}"}'
        response = requests.post(self.base_url, headers=self.headers, data=payload)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['data']['people']['name'], 'Luke Skywalker')

if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGraphQlApi)
    unittest.TextTestRunner(verbosity=2).run(suite)
