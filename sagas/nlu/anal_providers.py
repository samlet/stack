from typing import Text, Any, Dict, List, Union, Optional

from sagas.nlu.intf import Entity
import logging

logger = logging.getLogger(__name__)

def get_entity_mapping(doc, provider_name) -> Dict[int, Entity]:
    from sagas.nlu.rasa_procs import get_entities
    sents, doc=doc.sents, doc.doc
    ents: List[Entity]=get_entities(sents, rasa_entry=provider_name)
    running_offset = 0
    rs = {}
    for token in doc.words:
        word = token.text
        word_offset = sents.find(word, running_offset)
        if word_offset>-1:
            word_len = len(word)
            running_offset = word_offset + word_len
            logger.debug(f"{word} - ({word_offset}, {running_offset})")
            for ent in ents:
                start, end=ent.start, ent.end
                if word_offset>=start and running_offset<=end:
                    rs[token.index]=ent
    return rs

providers={'rasa_simple': get_entity_mapping}
def get_provider_by_name(name):
    return providers[name]

