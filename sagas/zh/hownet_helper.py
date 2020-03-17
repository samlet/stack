from typing import Text, Any, Dict, List, Union
import sagas.tracker_fn as tc
from pprint import pprint

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
    def vis(self, word:Text, word_info:bool=True, format:Text='tree'):
        """
        $ python -m sagas.zh.hownet_helper vis '大学生'
        $ python -m sagas.zh.hownet_helper vis '苹果'
        $ python -m sagas.zh.hownet_helper vis '杯子'
        $ python -m sagas.zh.hownet_helper vis '杯子' False json

        :param word:
        :param format:
        :return:
        """
        # from sagas.zh.hownet_procs import hownet_procs
        from sagas.tool.servant_delegator import Delegator
        # trees = hownet_procs.build_sememe_trees(word)
        trees=Delegator().sememes(word=word)
        if format=='json':
            for tree in trees:
                if word_info:
                    pprint(tree['word'])
                pprint(tree['tree'])
        else:
            vis_trees(trees, word_info=word_info)

if __name__ == '__main__':
    import fire
    fire.Fire(HowNetCli)


