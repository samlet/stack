from typing import Text, Any, Dict, List, Union
import sagas.tracker_fn as tc

def vis_trees(trees:List[Any]):
    from anytree.importer import DictImporter
    from anytree import RenderTree
    importer = DictImporter()
    for index, data in enumerate(trees):
        tree_root = importer.import_(data)
        tree = RenderTree(tree_root)
        tc.emp('green', "Display #{0} sememe tree".format(index))
        for pre, fill, node in tree:
            if node.role and node.role!='None':
                cl='magenta'
            else:
                cl='yellow'
            tc.emp(cl, "%s[%s]%s" % (pre, node.role, node.name))


class HowNetCli(object):
    def vis(self, word, format='tree'):
        """
        $ python -m sagas.zh.hownet_helper vis '大学生'
        :param word:
        :param format:
        :return:
        """
        # from sagas.zh.hownet_procs import hownet_procs
        from pprint import pprint
        from sagas.tool.servant_delegator import Delegator
        # trees = hownet_procs.build_sememe_trees(word)
        trees=Delegator().sememes(word=word)
        if format=='json':
            pprint(trees)
        else:
            vis_trees(trees)

if __name__ == '__main__':
    import fire
    fire.Fire(HowNetCli)


