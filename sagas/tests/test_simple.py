#!/usr/bin/env python
"""Unit test for ..."""
import requests
import unittest

class TestSimple(unittest.TestCase):
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

    def test_simple(self):
       print("just a test.")

        # self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSimple)
    unittest.TextTestRunner(verbosity=2).run(suite)
