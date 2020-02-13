from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

class Rules_zh(LangSpecBase):
    def predicate_rules(self):
        pat, actions_obj=(self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sz '你有多少文件'
            pat(5, name='possessions_file').verb(behaveof('have', 'v'),
                                                 a1=kindof('file/communication', 'n')),
            # $ sz '今天温度是九十度'
            pat(5, name='desc_temperature').verb(extract_for('temperature', 'a1'),
                                                 behaveof('be', 'v'),
                                                 a0=kindof('temperature', 'n')),
        ])

    def execute(self):
        super().execute()


