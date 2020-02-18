from pyknp import KNP
import codecs
import optparse
import pyknp
import six
import sys

from sagas.ja.knp_helper import tokens
import sagas.tracker_fn as tc

def draw_tree(bl, outf):
    assert isinstance(bl, pyknp.BList)

    tl = pyknp.TList()
    tags = bl.tag_list()
    for tag in tags:
        tl.push_tag(tag)
    nodelines = tl.sprint_tree().split(u"\n")[:-1]

    outf.write(u"# S-ID: %s\n" % bl.sid)

    for i, nl in enumerate(nodelines):
        outf.write(nl)
        outf.write(u"\t")
        outf.write(u"/ ")
        pas = tags[i].features.pas
        if pas is not None:
            outf.write(pas.cfid)
            outf.write(u"\t")
            for casename, arglist in sorted(pas.arguments.items()):
                for arg in arglist:
                    if arg.sid == bl.sid:
                        if hasattr(tags[arg.tid], 'head_prime_repname') \
                                and tags[arg.tid].head_prime_repname:
                            rep = tags[arg.tid].head_prime_repname
                        else:
                            rep = tags[arg.tid].repname
                    else:
                        rep = u"<sid=%s,tid=%s>" % (arg.sid, arg.tid)
                    outf.write(u"%s:%s " % (casename, rep))

        outf.write(u"/ ")
        rels = tags[i].features.rels
        if rels is not None:
            for rel in sorted(rels, key=lambda x: x.atype):
                outf.write(u"%s:%s " % (rel.atype, rel.target))
        outf.write(u"\n")

    outf.write(u"\n\n")


def draw_trees(inf, outf, lattice_format):
    juman_format = pyknp.JUMAN_FORMAT.DEFAULT
    if lattice_format:
        juman_format = pyknp.JUMAN_FORMAT.LATTICE_TOP_ONE
    lines = []
    for line in inf:
        lines.append(line)
        if line == u"EOS\n":
            bl = pyknp.BList(u"".join(lines), juman_format=juman_format)
            draw_tree(bl, outf)
            lines = []



class KnpProcs(object):
    def __init__(self):
        self.knp = KNP()

    def deps(self, sent):
        """
        $ python -m sagas.ja.knp_procs deps "望遠鏡で泳いでいる少女を見た。"
        $ python -m sagas.ja.knp_procs deps "どのおかずを注文したの？"
            どの/どの -> おかず/おかず
            おかず/おかず  -> 注文/ちゅうもん する/する
        :param sent:
        :return:
        """
        # "望遠鏡で泳いでいる少女を見た。"
        result = self.knp.parse(sent)

        for bnst in result.bnst_list():
            parent = bnst.parent
            if parent is not None:
                child_rep = " ".join(mrph.repname for mrph in bnst.mrph_list())
                parent_rep = " ".join(mrph.repname for mrph in parent.mrph_list())
                print(child_rep, "->", parent_rep)

    def predicates(self, sent):
        """
        $ python -m sagas.ja.knp_procs predicates "望遠鏡で泳いでいる少女を見た。"
        $ python -m sagas.ja.knp_procs predicates "私は望遠鏡で泳いでいる少女を見た。"
            述語: 泳いでいる
                格: ガ,  項: 少女  (項の基本句ID: 4)
            述語: 見た。
                格: ガ,  項: 私  (項の基本句ID: 0)
                格: ヲ,  項: 少女  (項の基本句ID: 4)
                格: デ,  項: 鏡  (項の基本句ID: 2)
        $ python -m sagas.ja.knp_procs predicates "私は海で泳いでいる少女を見た。"
            述語: 泳いでいる
                格: ガ,  項: 少女  (項の基本句ID: 3)
                格: デ,  項: 海  (項の基本句ID: 1)
            述語: 見た。
                格: ガ,  項: 私  (項の基本句ID: 0)
                格: ヲ,  項: 少女  (項の基本句ID: 3)
        :param sent:
        :return:
        """
        result = self.knp.parse(sent)

        for tag in result.tag_list():
            if tag.pas is not None:  # find predicate
                print('述語: %s' % ''.join(mrph.midasi for mrph in tag.mrph_list()))
                for case, args in tag.pas.arguments.items():  # case: str, args: list of Argument class
                    for arg in args:  # arg: Argument class
                        print('\t格: %s,  項: %s  (項の基本句ID: %d)' % (case, arg.midasi, arg.tid))

    def tree(self, sent):
        """
        $ python -m sagas.ja.knp_procs tree "望遠鏡で泳いでいる少女を見た。"
        :param sent:
        :return:
        """
        result = self.knp.parse(sent)
        outf = sys.stdout
        draw_tree(result, outf)

    def tokens(self, sents):
        """
        $ python -m sagas.ja.knp_procs tokens "望遠鏡で泳いでいる少女を見た。"
        $ python -m sagas.ja.knp_procs tokens "彼女は卵を食べる。"
        :param sents:
        :return:
        """
        print(','.join(tokens(sents)))

    def ner(self, line):
        """
        $ python -m sagas.ja.knp_procs ner "太郎は5月18日の朝9時に花子に会いに行った．"
        :param line:
        :return:
        """
        import re

        # KNP prepairing:
        # option (str) – KNP解析オプション (詳細解析結果を出力する-tabは必須。
        # 省略・照応解析を行う -anaphora, 格解析を行わず構文解析のみを行う -dpnd など)
        knp = pyknp.KNP(option="-tab -dpnd", jumanpp=False)

        def make_np_tagged_text(src_text: str):
            tagged_text = src_text  # copy
            result = knp.parse(src_text)  # tagging

            for tag in result.tag_list():
                if "NE:" in tag.fstring:  # if fstring has NE phrase
                    span=result.get_tag_span(tag.tag_id)
                    print('..', span,  tag.fstring)
                    # extract NE phrase
                    search_r=re.search("<NE:(.*):(.*)>", tag.fstring)
                    # tagged_ne_phrase = re.search("<NE:(.*):(.*)>", tag.fstring).group(0)
                    # ne_phrase = re.search("<NE:(.*):(.*)>", tag.fstring).group(2)
                    tagged_ne_phrase =search_r.group(0)
                    ne_phrase=search_r.group(2)

                    # overwrite to src text
                    tagged_text = tagged_text.replace(ne_phrase, tagged_ne_phrase)

            return tagged_text

        tc.emp('green', line)
        tc.emp('yellow', make_np_tagged_text(line))

if __name__ == '__main__':
    import fire
    fire.Fire(KnpProcs)
