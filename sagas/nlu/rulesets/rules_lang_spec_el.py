from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_el(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_el(Greek, 希腊语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sel 'Θα ήθελα μία μπύρα.'
            # $ sel 'Θα ήθελα ένα μεταλλικό νερό.'
            # $ sel 'Θα ήθελα έναν χυμό πορτοκάλι.'
            # $ sel 'Θα ήθελα έναν καφέ.'
            # $ sel 'Θα ήθελα έναν καφέ με γάλα.'
            # $ sel 'Θα ήθελα ένα τσάι.'
            # Data source: "At the restaurant 1"
            pat(5, name='behave_want').verb(
                behaveof('want', 'v'),
                obj=specsof('n', 'beverage', 'water', 'juice', 'cafe')),

        ])
    

