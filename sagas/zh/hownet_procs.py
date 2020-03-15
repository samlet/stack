class HowNetProcs(object):
    """
    See also: procs-hownet.ipynb
    """
    def __init__(self):
        import OpenHowNet
        self.hownet_dict = OpenHowNet.HowNetDict()

    def build_sememe_trees(self, word, K=None):
        """
        :param word: (str)The target word to be visualized in command line. Notice that single word may correspond to multiple HowNet annotations.
        :param K: (int)The maximum number of visualized words, ordered by id (ascending). Illegal number will be automatically ignored and the function will display all retrieved results.
        :return:
        """
        from OpenHowNet.SememeTreeParser import GenSememeTree
        from anytree.exporter import DictExporter, JsonExporter

        queryResult = list(self.hownet_dict[word])
        queryResult.sort(key=lambda x: x["No"])
        # print("Find {0} result(s)".format(len(queryResult)))
        if K is not None and K >= 1 and type(K) == int:
            queryResult = queryResult[:K]

        trees = []
        # exporter = JsonExporter(indent=2, sort_keys=True)
        exporter = DictExporter()
        for index, item in enumerate(queryResult):
            tree = GenSememeTree(item["Def"], word, returnNode=True)
            trees.append(exporter.export(tree))
        return trees

hownet_procs=HowNetProcs()

