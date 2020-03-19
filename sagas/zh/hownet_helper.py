from typing import Text, Any, Dict, List, Union, Set

from cachetools import TTLCache, cached
from dataclasses import dataclass
from sagas.tool.servant_delegator import Delegator
import sagas.tracker_fn as tc
from pprint import pprint
import logging

logger = logging.getLogger(__name__)

@dataclass
class SenseSyn:
    id: str
    text: str


@dataclass
class SenseWord:
    definition: str
    en_grammar: str
    zh_grammar: str
    en_word: str
    zh_word: str
    id: str
    syns: List[SenseSyn]


@dataclass
class SenseNode:
    role: str
    name: str
    children: List['SenseNode']

    def role_in(self, role_name):
        return [c for c in self.children if c.role == role_name]

    @property
    def all_roles(self):
        return {c.role for c in self.children}


@dataclass
class SenseTree:
    root: SenseNode
    inherits: List[SenseNode]
    roles: Dict[Text, Set[Text]]
    word: SenseWord

    def cat_of(self, cat):
        """
        >>> st.cat_of('human|人')
        :param cat:
        :return:
        """
        rs = [ci for ci in self.inherits if ci.name == cat]
        return len(rs) > 0

    def has_role(self, **kwargs):
        """
        >>> st.has_role(agent='study|学习')
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            if k not in self.roles:
                return False
            role_data = self.roles[k]
            if v not in role_data:
                return False
        return True


def build_sense_word(word:Dict[Text, Any]) -> SenseWord:
    s_word = SenseWord(definition=word['Def'],
                       en_grammar=word['en_grammar'],
                       zh_grammar=word['ch_grammar'],
                       en_word=word['en_word'],
                       zh_word=word['ch_word'],
                       id=word['No'],
                       syns=[SenseSyn(row['id'], row['text']) for row in word['syn']]
                       )
    return s_word

def build_node(tree_data, inherits, roles):
    role=tree_data['role']
    node=SenseNode(role=tree_data['role'] if role!='None' else '',
                   name=tree_data['name'],
                   children=[build_node(c, inherits, roles) for c in tree_data['children']] if 'children' in tree_data else []
                  )
    if role=='None':
        inherits.append(node)
    else:
        if role in roles:
            roles[role].add(node.name)
        else:
            roles[role]={node.name}
    return node

def build_trees(json_trees:List[Dict[Text, Any]]) -> List[SenseTree]:
    trees=[]
    for data in json_trees:
        logger.debug(f"data keys {list(data.keys())}")
        tree_data = data['tree']
        word_data=data['word']

        inherits = []
        roles = {}
        root = build_node(tree_data, inherits, roles)
        word=build_sense_word(word_data)
        s_tree = SenseTree(root=root, inherits=inherits, roles=roles, word=word)
        trees.append(s_tree)

    return trees

def get_words(text: Text):
    from sagas.tool.servant_delegator import Delegator
    words = Delegator().sense(word=text)
    return words


@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_word_sense(text: Text) -> List[SenseWord]:
    words=get_words(text)
    return [build_sense_word(item) for item in words]

word_sets=lambda text: [(word.zh_word, word.zh_grammar,
                              word.en_word, word.en_grammar)
                             for word in get_word_sense(text)]

@cached(cache={})
def get_trees(text: Text) -> List[SenseTree]:
    from OpenHowNet.SememeTreeParser import GenSememeTree

    trees = []
    # 只需要解析不同的树即可
    words=get_words(text)
    uniques = {item['Def']: item['No'] for item in words}
    unique_rs = [item for item in words if item['No'] in uniques.values()]
    for item in unique_rs:
        tree = GenSememeTree(item["Def"], text)
        trees.append({"word": item, "tree": tree})
    sts = build_trees(trees)
    return sts

def vis_trees(trees:List[Dict[Text, Any]], word_info=True):
    from anytree.importer import DictImporter
    from anytree import RenderTree
    importer = DictImporter()
    for index, data in enumerate(trees):
        if word_info:
            pprint(data['word'])
        tree_root = importer.import_(data['tree'])
        tree = RenderTree(tree_root)
        tc.emp('green', "Display #{0} sememe tree".format(index))
        for pre, fill, node in tree:
            if node.role and node.role!='None':
                cl='magenta'
                role=node.role
            else:
                cl='yellow'
                role='✔'
            tc.emp(cl, "%s%s: %s" % (pre, role, node.name))

def expand_tree(tree, property_name:Text, layer:int, is_root=True):
    res = set()
    if layer == 0:
        return res

    # special process with the root node
    if isinstance(tree, dict):
        target = [tree]
    else:
        target = tree

    for item in target:
        try:
            if not is_root:
                res.add(item["name"])
                # res.add(item["name"].split("|")[choice])

            if "children" in item:
                res |= expand_tree(item["children"],
                                   property_name,
                                   layer - 1, is_root=False)
        except IndexError:
            continue
    return res

class HowNetCli(object):
    def vis(self, word:Text, word_info:bool=True, format:Text='tree', merge:bool=True):
        """
        $ python -m sagas.zh.hownet_helper vis '大学生'
        $ python -m sagas.zh.hownet_helper vis '苹果'
        $ python -m sagas.zh.hownet_helper vis '杯子'
        $ python -m sagas.zh.hownet_helper vis '杯子' False json
        $ hownet 合作 True tree False  # 因为是按def合并的(所以tree是相同的), 单词属性有所不同

        :param word:
        :param format:
        :return:
        """
        # from sagas.zh.hownet_procs import hownet_procs
        # trees = hownet_procs.build_sememe_trees(word)
        trees=Delegator().sememes(word=word, merge=merge)
        if format=='json':
            for tree in trees:
                if word_info:
                    pprint(tree['word'])
                pprint(tree['tree'])
        else:
            vis_trees(trees, word_info=word_info)

    def sense(self, word:Text, info='raw'):
        """
        $ python -m sagas.zh.hownet_helper sense '合作'
        :param word:
        :return:
        """
        words=Delegator().sense(word=word)
        pprint(words)

    def word_sets(self, word:Text):
        """
        $ python -m sagas.zh.hownet_helper word_sets '合作'
        :param word:
        :return:
        """
        pprint(word_sets(word))

if __name__ == '__main__':
    import fire
    fire.Fire(HowNetCli)


