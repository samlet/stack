from unittest import TestCase

from sagas.nlu.words_servant import get_synsets_as_json


class TestGet_synsets_as_json(TestCase):
    def test_get_synsets_as_json(self):
        # self.fail()
        r=get_synsets_as_json('id', 'membaca', 'v')
        print('\n1.', r)
        r = get_synsets_as_json('id', 'menbaca', 'v')
        print('\n2.', r)
        r = get_synsets_as_json('id', 'membaca/menbaca', 'v')
        print('\n3.', r)

