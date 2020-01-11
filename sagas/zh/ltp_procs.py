from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
import sys, os
import pandas as pd
import sagas

def join_words(words, arg_range):
    return ''.join([str(words[idx]) for idx in range(arg_range.start, arg_range.end+1)])

def explain(arg_name):
    if arg_name=='A0':
        return '动作的施事'
    elif arg_name=='A1':
        return '动作的影响'
    return arg_name

# def extract_predicates(words, roles, verbose=False):
#     predicts = []
#     for role in roles:
#         if verbose:
#             print(f"{words[role.index]}({role.index})", '->', "".join(
#                 ["%s:(%d,%d) _ " % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
#         args = []
#         for arg in role.arguments:
#             # print('\t', arg.name, arg.range.start, arg.range.end)
#             cnt = join_words(words, arg.range)
#             if verbose:
#                 print('\t', explain(arg.name), '☞', cnt)
#             # print('\t', '----')
#             args.append({'name': arg.name, 'value': cnt, 'start': arg.range.start, 'end': arg.range.end})
#         predicts.append({'index': role.index, 'predicate': words[role.index],
#                          'args': args})
#     return predicts

def word_chunk(words, arg_range):
    return [str(words[idx]) for idx in range(arg_range.start, arg_range.end+1)]

def get_feats(postags, i):
    from sagas.nlu.uni_impl_ltp import get_pos_mapping
    # return [postags[i], get_pos_mapping(postags[i])]
    pos_tr=get_pos_mapping(postags[i])
    return ['c_{}'.format(pos_tr).lower(),
            'x_{}'.format(postags[i]).lower()]

def extract_predicates(words, roles, postags, arcs, verbose=False):
    from pypinyin import lazy_pinyin
    from sagas.nlu.uni_impl_ltp import get_pos_mapping

    predicts = []
    predict_tuples=[]
    for role in roles:
        if verbose:
            print(f"{words[role.index]}({role.index})", '->', "".join(
                ["%s:(%d,%d) _ " % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
        args = []
        domains=[]
        for arg in role.arguments:
            # print('\t', arg.name, arg.range.start, arg.range.end)
            chunk = word_chunk(words, arg.range)
            main_word=words[arg.range.end]
            # if verbose:
            #     print('\t', arg.name, '☞', cnt)
            # print('\t', '----')
            rel=arg.name.lower()
            args.append({'name': rel, 'chunk': chunk, 'value': str(main_word),
                         'start': arg.range.start, 'end': arg.range.end})
            # ['rel', 'index', 'text', 'lemma', 'children', 'features']
            feats=get_feats(postags, arg.range.end)
            domains.append((rel, arg.range.end, str(main_word), str(main_word),
                           chunk, feats))
        lemma=words[role.index]
        predicts.append({'index': role.index, 'predicate': lemma,
                         'args': args})
        i=role.index
        dependency_relation=str(arcs[i].relation).lower()
        governor=arcs[i].head
        predict_tuples.append({'type':'predicate', 'lemma':lemma, 'index': i,
                               'phonetic':' '.join(lazy_pinyin(lemma)), 'word':lemma,
                               'rel': dependency_relation, 'governor': governor,
                               'pos': get_pos_mapping(postags[i]).lower(),
                               'domains': domains, 'stems':[]})
    return predicts, predict_tuples

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

    def parse(self, sentence):
        words = self.segmentor.segment(sentence)
        postags = self.postagger.postag(words)
        arcs = self.parser.parse(words, postags)
        roles = self.labeller.label(words, postags, arcs)
        netags = self.recognizer.recognize(words, postags)
        return words, postags, arcs, roles, netags

    def tokens(self, sents):
        words = self.segmentor.segment(sents)
        return [str(w) for w in words]

    def analyse(self, sentence, verbose=False, show_roles=True):
        """
        $ python -m sagas.zh.ltp_procs analyse '中国进出口银行与中国银行加强合作。'
        $ python -m sagas.zh.ltp_procs analyse '国务院总理李克强调研上海外高桥时提出，支持上海积极探索新机制。'
        $ ltp '我是学生'
        :param sentence:
        :return:
        """
        from colorama import Fore, Back, Style
        from tabulate import tabulate
        import sagas

        pd.set_option('display.unicode.ambiguous_as_wide', True)
        pd.set_option('display.unicode.east_asian_width', True)

        # words = self.segmentor.segment(sentence)
        # postags = self.postagger.postag(words)
        # arcs = self.parser.parse(words, postags)
        # roles = self.labeller.label(words, postags, arcs)
        # netags = self.recognizer.recognize(words, postags)
        words, postags, arcs, roles, netags=self.parse(sentence)

        # roles
        print('❶ roles for', " ".join(words))
        # roles = self.labeller.label(words, postags, arcs)

        predicts=extract_predicates(words, roles, postags, arcs, verbose=False)
        print(predicts)

        # dep-parse
        if not show_roles:
            print('❷ dep parse')
            rs = []
            for i in range(len(words)):
                if verbose:
                    print("%s --> %s|%s|%s|%s" % (words[int(arcs[i].head) - 1], words[i], \
                                                  arcs[i].relation, postags[i], netags[i]))
                rs.append((words[int(arcs[i].head) - 1], words[i], \
                           arcs[i].relation, postags[i], netags[i]))
            df=sagas.to_df(rs, ['弧头', '弧尾', '依存关系', '词性', '命名实体'])
            df['命名实体'] = Fore.RED + Style.BRIGHT + df['命名实体'].astype(str) + Style.RESET_ALL
            # print(df)
            print(tabulate(df, headers='keys', tablefmt='psql'))

        else:
            print('❷ tokens')

            # arrange roles to a column
            # https://github.com/HIT-SCIR/pyltp/issues/152
            srl_as_tag_matrix = [['*'] * len(roles) for _ in sentence]
            for predicate_id, role in enumerate(roles):
                srl_as_tag_matrix[role.index][predicate_id] = '(V*)'
                for arg in role.arguments:
                    srl_as_tag_matrix[arg.range.start][predicate_id] = '(%s*' % arg.name
                    srl_as_tag_matrix[arg.range.end][predicate_id] += ')'

            rs = []
            for id, (word, pos, arc, ne, role) in enumerate(zip(words, postags, arcs, netags, srl_as_tag_matrix)):
                rs.append(([str(id), word, pos, str(arc.head), arc.relation, ne, ', '.join(role)]))
            sagas.print_rs(rs, ['id','word','pos','head','rel','ne','role'])

ltp=LtpProcs()

if __name__ == '__main__':
    import fire
    fire.Fire(LtpProcs)
