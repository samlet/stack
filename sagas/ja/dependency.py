import CaboCha
import romkan
from cabocha.analyzer import CaboChaAnalyzer

class JaDeps(object):
    def analyse_feature(self, feat):
        result="@g"
        if feat.startswith("名詞,数"):
            result="@num"
        elif feat.startswith("名詞,サ変接続"):
            result="@nc"
        elif feat.startswith("名詞"):
            result="@n"
        elif feat.startswith("動詞"):
            result="@v"
        # 形容詞
        elif feat.startswith("形容詞"):
            result="@adj"
        return result

    def join_tokens(self, chunk):
        l=[]
        for token in chunk:
            if not token.feature.startswith("助") and \
                not token.feature.startswith("記号"):
                l.append(token.surface)
        return ''.join(l)

    def join_nc_tokens(self, chunk):
        l=[]
        for token in chunk:
            if not token.feature.startswith("助動詞,*") and \
                not token.feature.startswith("助詞,係助詞") and \
                not token.feature.startswith("助詞,格助詞") and \
                not token.feature.startswith("記号"):
                l.append(token.surface)
        return ''.join(l)

    def get_prefix(self, chunk):
        token=chunk.tokens[-1]
        last=token.surface
        feat=chunk.tokens[0].feature

        if feat.startswith("名詞,非自立"):
            return 'con:'

        if last=='は':
            return "actor:"
        elif last=='を' or last=='に':
            return "obj:"
        elif last=='が':
            return "exist:"
        elif last=='の':
            return "def:"
        elif last=='まで':
            # print(len(chunk.prev_links))
            if chunk.has_prev_links():
                prev=(chunk.prev_links[0])
                prevlast=prev.tokens[-1].surface
                if prevlast=='から':
                    return "range:"+self.join_tokens(prev)
            return "till:"
        else:
            return ""

    def get_first_token(self, chunk):
        token=chunk.tokens[0]
        kan=token.feature.split(',')[-2]
        if kan=='*':
            kan=token.surface
        return (romkan.to_roma(kan))

    def create_parts(self, sentence, romas):
        func = "_noname_"
        analyzer = CaboChaAnalyzer()
        tree = analyzer.parse(sentence)
        l = []
        mainPart = 0
        for chunk in tree:
            for token in chunk:
                kan = token.feature.split(',')[-2]
                if kan == '*':
                    kan = token.surface
                romas.append(romkan.to_roma(kan))
            if chunk.link == -1:
                mainPart = chunk.id
                func = self.get_first_token(chunk)
        for chunk in tree:
            curword = chunk.tokens[0].surface
            curfeature = chunk.tokens[0].feature
            feat = self.analyse_feature(curfeature)
            if feat == '@num' or feat == '@n':
                curword = self.join_tokens(chunk)
            elif feat == '@nc':
                curword = self.join_nc_tokens(chunk)
            elif feat == '@v':
                parts = curfeature.split(',')
                raw = parts[-3]
                if raw != '*':
                    curword = raw

            ## main part
            if chunk.link == -1:
                prefix = ""
                if feat == '@v':
                    prefix = "act:"
                elif feat == '@adj':
                    prefix = "desc:"
                elif feat == '@n':
                    prefix = "prop:"
                l.append(prefix + "*" + curword + feat)
            elif chunk.link == mainPart:
                l.append(self.get_prefix(chunk) + "+" + curword + feat)
            else:
                l.append("." + curword + feat)
        result = func + '(' + ", ".join(l) + ')'
        return result

    def tree(self, sentence):
        # from tasks import oplog
        # sentence = get_from_clip()

        logs = []
        c = CaboCha.Parser()
        tree = c.parse(sentence)
        treelog = tree.toString(CaboCha.FORMAT_TREE_LATTICE)
        logs.append(treelog)
        print(treelog)

        romas = []
        result = "% " + sentence
        partlog = "✆ " + self.create_parts(sentence, romas)
        romalog = "ﺴ " + " ".join(romas)

        logs.append(result)
        logs.append(partlog)
        logs.append(romalog)
        print(result)
        print(partlog)
        print(romalog)

