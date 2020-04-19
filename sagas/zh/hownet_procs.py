from typing import Text, Any, Dict, List, Union

pos_mapping={'a': 'adj', 'n':'noun', 'v': 'verb', 'r': 'adv'}

def pos_filter(l:List[Any], pos:Text):
    if pos == '*' or pos not in pos_mapping: return l
    pos_w = pos_mapping[pos]
    return [e for e in l if e['en_grammar'] == pos_w]

class HowNetProcs(object):
    """
    See also: procs-hownet.ipynb
    """
    def __init__(self):
        import OpenHowNet
        self.hownet_dict = OpenHowNet.HowNetDict()

    def get_sense(self, word, pos='*') -> List[Any]:

        if '/' in word:
            rs=[]
            for w in word.split('/'):
                rs.extend(pos_filter(self.hownet_dict[w], pos))
            return rs
        else:
            return pos_filter(self.hownet_dict[word], pos)

    def get_sense_by_id(self, id) -> List[Any]:
        return self.hownet_dict.ids[id]

    def build_sememe_trees(self, word, merge=True, K=None, pos='*') -> List[Dict[Text, Any]]:
        """
        :param word: (str)The target word to be visualized in command line. Notice that single word may correspond to multiple HowNet annotations.
        :param K: (int)The maximum number of visualized words, ordered by id (ascending). Illegal number will be automatically ignored and the function will display all retrieved results.
        :return:
        """
        from OpenHowNet.SememeTreeParser import GenSememeTree
        from anytree.exporter import DictExporter, JsonExporter

        query_result:List = pos_filter(self.hownet_dict[word], pos)
        query_result.sort(key=lambda x: x["No"])
        # query_result.sort(key=lambda x: x["No"], reverse=True)
        # print("Find {0} result(s)".format(len(queryResult)))
        if K is not None and K >= 1 and type(K) == int:
            query_result = query_result[:K]

        if merge:
            uniques={item['Def']: item['No'] for item in query_result}
            query_result=[item for item in query_result if item['No'] in uniques.values()]

        trees = []
        # exporter = JsonExporter(indent=2, sort_keys=True)
        exporter = DictExporter()
        for index, item in enumerate(query_result):
            tree = GenSememeTree(item["Def"], word, returnNode=True)
            # trees.append(exporter.export(tree))
            trees.append({"word": item, "tree": exporter.export(tree)})
        return trees

hownet_procs=HowNetProcs()

