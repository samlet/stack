from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
import sys, os
import pandas as pd
import sagas

descs='''标记	说明
ADV	adverbial, default tag ( 附加的，默认标记 )
BNE	beneﬁciary ( 受益人 )
CND	condition ( 条件 )
DIR	direction ( 方向 )
DGR	degree ( 程度 )
EXT	extent ( 扩展 )
FRQ	frequency ( 频率 )
LOC	locative ( 地点 )
MNR	manner ( 方式 )
PRP	purpose or reason ( 目的或原因 )
TMP	temporal ( 时间 )
TPC	topic ( 主题 )
CRD	coordinated arguments ( 并列参数 )
PRD	predicate ( 谓语动词 )
PSR	possessor ( 持有者 )
PSE	possessee ( 被持有 )'''

def get_role_defs():
    desc_rs = []
    for desc in descs.split('\n')[1:]:
        desc_rs.append(desc.split('\t'))
    return sagas.to_df(desc_rs, ['mark', 'description'])

def join_words(words, arg_range):
    return ''.join([str(words[idx]) for idx in range(arg_range.start, arg_range.end+1)])

def explain(arg_name):
    if arg_name=='A0':
        return '动作的施事'
    elif arg_name=='A1':
        return '动作的影响'
    return arg_name

class LtpProcs(object):
    def __init__(self):
        MODELDIR = '/pi/ai/ltp/ltp_data_v3.4.0'
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(MODELDIR, "cws.model"))
        self.postagger = Postagger()
        self.postagger.load(os.path.join(MODELDIR, "pos.model"))
        self.parser = Parser()
        self.parser.load(os.path.join(MODELDIR, "parser.model"))
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(MODELDIR, "ner.model"))
        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(MODELDIR, "pisrl.model"))

    def release(self):
        self.segmentor.release()
        self.postagger.release()
        self.parser.release()
        self.recognizer.release()
        self.labeller.release()

    def analyse(self, sentence):
        """
        $ python -m sagas.zh.ltp_procs analyse '中国进出口银行与中国银行加强合作。'
        $ python -m sagas.zh.ltp_procs analyse '国务院总理李克强调研上海外高桥时提出，支持上海积极探索新机制。'
        $ ltp '我是学生'
        :param sentence:
        :return:
        """
        from colorama import Fore, Back, Style
        from tabulate import tabulate
        pd.set_option('display.unicode.ambiguous_as_wide', True)
        pd.set_option('display.unicode.east_asian_width', True)

        words = self.segmentor.segment(sentence)
        postags = self.postagger.postag(words)
        arcs = self.parser.parse(words, postags)
        roles = self.labeller.label(words, postags, arcs)
        netags = self.recognizer.recognize(words, postags)

        # roles
        print('❶ roles for', " ".join(words))
        roles = self.labeller.label(words, postags, arcs)
        for role in roles:
            print(role.index, '->', "".join(
                ["%s:(%d,%d) _ " % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
            for arg in role.arguments:
                # print(''.join(words[arg.range.start:arg.range.end]))
                print(arg.name, arg.range.start, arg.range.end)
                # print(arg.name, words[arg.range.start], words[arg.range.end])
                print(explain(arg.name), join_words(words, arg.range))
                print('----')

        # dep-parse
        print('❷ dep parse')
        rs = []
        for i in range(len(words)):
            print("%s --> %s|%s|%s|%s" % (words[int(arcs[i].head) - 1], words[i], \
                                          arcs[i].relation, postags[i], netags[i]))
            rs.append((words[int(arcs[i].head) - 1], words[i], \
                       arcs[i].relation, postags[i], netags[i]))
        df=sagas.to_df(rs, ['弧头', '弧尾', '依存关系', '词性', '命名实体'])
        df['命名实体'] = Fore.RED + Style.BRIGHT + df['命名实体'].astype(str) + Style.RESET_ALL
        # print(df)
        print(tabulate(df, headers='keys', tablefmt='psql'))

if __name__ == '__main__':
    import fire
    fire.Fire(LtpProcs)
