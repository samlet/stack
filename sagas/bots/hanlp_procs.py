from py4j.java_gateway import JavaGateway, JavaObject, GatewayParameters
from py4j.java_gateway import java_import, get_field

'''
Usage:
from sagas.bots.hanlp_procs import Hanlp, hanlp, hanlp_c
'''

class Hanlp(object):
    def __init__(self):
        host="localhost"
        port=2333
        callback_port=2334
        self.gateway = JavaGateway(python_proxy_port=callback_port,
                              gateway_parameters=GatewayParameters(address=host, port=port, auto_field=True))
        j = self.gateway.new_jvm_view()
        java_import(j, 'com.hankcs.hanlp.*')
        java_import(j, 'java.util.*')
        java_import(j, 'com.hankcs.hanlp.util.*')
        java_import(j, 'com.hankcs.hanlp.utility.*')
        java_import(j, 'com.hankcs.hanlp.corpus.tag.Nature')
        java_import(j, 'com.hankcs.hanlp.corpus.dependency.CoNll.CoNLLWord')
        java_import(j, "com.hankcs.hanlp.tokenizer.NLPTokenizer")
        self.j=j
        self.helper = self.gateway.entry_point.helper()

    def get_pinyin(self, text):
        return self.j.HanLP.convertToPinyinList(text)

    def set_nature(self, nature_name, words):
        pcNature = self.j.Nature.create(nature_name)
        nature_c = self.j.Nature
        natures = self.gateway.new_array(nature_c, 1)
        natures[0] = pcNature
        for word in words:
            self.j.LexiconUtility.setAttribute(word, natures)

    def describe_rel(self, word, result):
        if word.DEPREL == "主谓关系":
            result.append("\tactor: {}".format(word.LEMMA))
        elif word.DEPREL == "动宾关系":
            result.append("\tobject: {}".format(word.LEMMA))
        elif word.DEPREL == "标点符号":
            pass
        else:
            result.append("\trel.{}({}): {}".format(word.POSTAG, word.DEPREL, word.LEMMA))

    def get_pinyin_tone(self, sentence):
        pinyin_list = self.j.HanLP.convertToPinyinList(sentence)
        l = []
        for pinyin in pinyin_list:
            l.append("%s" % pinyin.getPinyinWithToneMark())
        return (" ".join(l))

    def parse_tree(self, sentence):
        conll = self.j.HanLP.parseDependency(sentence)
        coreindex = 0
        result = []
        for word in conll.iterator():
            if word.HEAD == self.j.CoNLLWord.ROOT:
                coreindex = word.ID
                result.append("core: {} - {}".format(word.POSTAG, word.LEMMA))
        for word in conll.iterator():
            if word.HEAD.ID == coreindex:
                self.describe_rel(word, result)

        result.append("⊕ " + str(self.j.NLPTokenizer.analyze(sentence)))
        result.append("⊙ " + str(self.j.NLPTokenizer.analyze(sentence).translateLabels()))
        result.append("ﺴ " + self.get_pinyin_tone(sentence))
        result.append("☫ " + self.j.HanLP.convertToTraditionalChinese(sentence))
        result.append("% " + sentence)
        return '\n'.join(result), conll

    def print_deps(self, conll):
        from tabulate import tabulate
        table_header = ['a', 'rel', 'b']
        table_data = []

        # 顺序遍历
        # sentence = self.j.HanLP.parseDependency(raw)
        wordArray = conll.getWordArray()
        for word in wordArray:
            # print("%s --(%s)--> %s"%(word.LEMMA, word.DEPREL, word.HEAD.LEMMA))
            table_data.append((word.LEMMA, word.DEPREL, word.HEAD.LEMMA))
        print(tabulate(table_data, headers=table_header, tablefmt='psql'))


hanlp=Hanlp()
hanlp_c=hanlp.j.HanLP

class HanlpProcs(object):
    def tree(self, sentence):
        """
        $ python -m sagas.bots.hanlp_procs tree '苹果电脑可以运行开源阿尔法狗代码吗'
        :param sentence:
        :return:
        """

        hanlp.set_nature('tech', ["苹果电脑", "阿尔法狗"])
        result, conll=hanlp.parse_tree(sentence)
        print(result)
        hanlp.print_deps(conll)

    def backtrace(self, raw, index=0):
        """
        $ python -m sagas.bots.hanlp_procs backtrace '苹果电脑可以运行开源阿尔法狗代码吗'
        :param raw:
        :param index:
        :return:
        """
        # 可以直接遍历子树，从某棵子树的某个节点一路遍历到虚根
        sentence = hanlp.j.HanLP.parseDependency(raw)
        wordArray = sentence.getWordArray()
        head = wordArray[index]
        while head is not None:
            if head == hanlp.j.CoNLLWord.ROOT:
                print(head.LEMMA)
            else:
                print("%s --(%s)--> " % (head.LEMMA, head.DEPREL))
            head = head.HEAD

    def deps(self, raw):
        """
        $ python -m sagas.bots.hanlp_procs deps '苹果电脑可以运行开源阿尔法狗代码吗'
        :param raw:
        :return:
        """
        # 顺序遍历
        sentence = hanlp.j.HanLP.parseDependency(raw)
        wordArray = sentence.getWordArray()
        for word in wordArray:
            print("%s --(%s)--> %s" % (word.LEMMA, word.DEPREL, word.HEAD.LEMMA))


if __name__ == '__main__':
    import fire
    fire.Fire(HanlpProcs)
