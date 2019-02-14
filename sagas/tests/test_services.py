#!/usr/bin/env python
"""Unit test for ..."""
import requests
import unittest
from sagas.ofbiz.services import OfService, MetaService
from sagas.ofbiz.entities import MetaEntity

class TestServices(unittest.TestCase):
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

    def test_product(self):
        ms = OfService()
        print(ms._name)
        # ok, result=ms.createProduct(userLogin=finder.user,
        ok, result = ms.createProduct(
            internalName='Test_product',
            productTypeId='GOOD')
        print(ok, result)
        product_id = result['productId']
        ok, result = ms.updateProduct(productId=product_id,
                                      productName='Test_name_B',
                                      description='Updated description')
        print(ok, result)

        # product_id = "10013"
        entity = MetaEntity("Product")
        rec = entity.find_one(productId=product_id)
        print(rec['description'])

    def test_meta(self):
        ms = MetaService("updateProduct")
        # print(ms.parameters)
        print(ms.inputs)

if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestServices)
    unittest.TextTestRunner(verbosity=2).run(suite)
