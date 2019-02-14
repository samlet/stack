#!/usr/bin/env python
"""Unit test for ..."""
import json

import requests
import unittest
from sagas.ofbiz.movies import schema
import uuid
from sagas.ofbiz.builder import abbrev

def rand_id():
    return abbrev("f_"+str(uuid.uuid4()), 15)

q1 = '''
{
  movies (limit:3, offset:2) {
    title
    saMovieGenresAppl{
        movieGenresId
    }
  }
}
'''.strip()
q2 = '''
{
  movies {
    title
    saMovieGenresAppl{
        movieGenresId
    }
  }
}
'''.strip()
q3='''
{
  movies (limit:10, offset:0) {
    movieId
    voteAverage
    title
    posterPath
    overview
    saMovieGenresAppl{
        movieGenresId
    }
  }
}
'''.strip()

m1 = '''
mutation myFirstMutation {
    createTestingType(testingTypeData: {testingTypeId:"(id)"}) {
        testingTypeId
        lastUpdatedStamp
        __typename
    }
}
'''.replace("(id)", rand_id()).strip()

class TestMovies(unittest.TestCase):
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

    def test_movie_schema(self):
        result = schema.execute(q1)
        print(json.dumps(result.data, indent=2, ensure_ascii=False))

    def test_movie_mutations(self):
        result = schema.execute(m1)
        print(json.dumps(result.data, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    # Test api endpoints
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMovies)
    unittest.TextTestRunner(verbosity=2).run(suite)
