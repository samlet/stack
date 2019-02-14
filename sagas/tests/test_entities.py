#!/usr/bin/env python
"""Unit test for ..."""
import requests
import unittest
from sagas.ofbiz.entities import MetaEntity

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
        entity = MetaEntity("Product")
        print(entity.primary)
        rec = entity.find_one(productId='10005')
        print(rec['internalName'])
        recs = entity.find_list(5, 0)
        print(len(recs))
        for r in recs:
            print(r['internalName'])

        product_id = "10013"
        entity = MetaEntity("Product")
        rec = entity.find_one(productId=product_id)
        print(rec['description'])

if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSimple)
    unittest.TextTestRunner(verbosity=2).run(suite)
