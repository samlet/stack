#!/usr/bin/env python
"""Unit test for api module GraphQL queries."""
import requests
import unittest
from tabulate import tabulate

from sagas.ofbiz.connector import OfbizConnector
from sagas.ofbiz.finder import Finder

class TestOfbizApi(unittest.TestCase):
    """Class to execute unit tests for api.py."""

    @classmethod
    def setUpClass(self):
        """Set up function called when class is consructed."""
        self.base_url = 'http://127.0.0.1:5000/graphql'
        self.headers = {'content-type': 'application/json'}

        self.oc = OfbizConnector()
        self.finder = Finder(self.oc)

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

    def test_simple(self):
        print(".. simple")

    def test_model_entity(self):
        entity_name="OfbizDemo"
        ent = self.oc.delegator.getModelEntity(entity_name)
        print(ent.getPlainTableName(), ent.getTitle(), ent.getDescription())

        entity_name = "SagasType"
        ent = self.oc.delegator.getModelEntity(entity_name)
        print(ent.getPlainTableName(), ent.getTitle(), ent.getDescription())

        entity_name = "SaMovie"
        ent = self.oc.delegator.getModelEntity(entity_name)
        print(ent.getPlainTableName(), ent.getTitle(), ent.getDescription())

    def test_find_list(self):
        rows=self.finder.find_list("SaMovie", 5, 0)
        for row in rows:
            print(row.get("movieId"), row.get("title"))

if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOfbizApi)
    unittest.TextTestRunner(verbosity=2).run(suite)

