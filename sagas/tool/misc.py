from time import sleep
import requests
from sagas.conf.conf import cf
import sagas.tracker_fn as tc
from sagas.nlu.rules_meta import build_meta
from sagas.nlu.utils import fix_sents, join_text
import logging

from sagas.tool import color_print
from pprint import pprint

logger = logging.getLogger(__name__)

merge_args=lambda args : ' '.join([str(arg[0]) if isinstance(arg, tuple) else arg for arg in args])

def print_terms(sents, result):
    from termcolor import colored
    for verb in result['verbs']:
        sents = sents.replace(verb[0], colored(verb[0], 'green'))
    for item, value in result.items():
        if 'subj' in item:
            sents = sents.replace(value, colored(value, 'red'))
        if 'obj' in item:
            sents = sents.replace(value, colored(value, 'blue'))
        if 'cop' in item:
            sents = sents.replace(value, colored(value, 'magenta'))
        if 'obl' in item:
            sents = sents.replace(value, colored(value, 'yellow'))
    tc.info('%s: %s' % (result['lang'], sents))

def print_terms_zh(sents, result):
    from termcolor import colored
    for verb in result['verbs']:
        sents = sents.replace(verb, colored(verb, 'green'))
    for item, value in result.items():
        if 'sbv' in item:
            sents = sents.replace(value, colored(value, 'red'))
        if 'ob' in item:
            sents = sents.replace(value, colored(value, 'blue'))
        # if 'cop' in item:
        #     sents = sents.replace(value, colored(value, 'magenta'))
    tc.info('%s: %s' % (result['lang'], sents))

# stem_filters=['obj', 'nsubj']
def print_stem_chunks(r):
    from termcolor import colored
    for stem in r['stems']:
        # if stem[0] in stem_filters:
        # stem[1]是一个列表, 包含了所有的word-lemmas, 在这里只打印出非空集的stem-chunk
        if len(stem[1])>1:
            value=' '.join(stem[1])
            # stem[0]是成分名称, 比如obj/obl/nsubj/...
            # tc.info('%s ->'%stem[0], colored(value, 'green'), file=file)
            tc.label('%s ->'%stem[0], value)

# others: 'nsubj'
display_synsets_opts=['obl', 'obj', 'iobj', 'nmod',
                      'obl:arg',
                      # $ ses 'La reina decía que la aldea era bonita.'
                      'ccomp',
                      # $ sz '现在是几点？'
                      # $ sz '昨天是星期几？'
                      'sbv', 'vob',
                      # predicts
                      'a0', 'a1',
                      'ガ',
                      'head_acl',  # governor elements
                      ]
def display_synsets(theme, meta, r, lang, collect=False):
    from sagas.nlu.nlu_cli import retrieve_word_info
    # from termcolor import colored

    from sagas.nlu.inspector_common import Context
    ctx=Context(meta, r['domains'])

    resp=[]
    # word = r['lemma']
    def retrieve(word, indicator, pos='*'):
        rs = retrieve_word_info('get_synsets', word, lang, pos=pos)
        if len(rs) > 0:
            if collect:
                resp.append({'word':word, 'indicator':indicator, 'comments':rs})
            else:
                comments=', '.join(rs)[:25]
                # tc.info('♥ %s(%s): %s...' % (colored(word, 'magenta'), indicator, comments))
                tc.emp('magenta', '♥ %s(%s): %s...' % (word, indicator, comments))
                resp.append('♥ %s(%s): %s...' % (word, indicator, comments))
            return True
        return False

    retrieve(f"{r['word']}/{r['lemma']}", theme, 'v' if theme=='[verb]' else '*')
    if 'head' in meta:
        # print('.........')
        retrieve(meta['head'], 'head')
    for opt in display_synsets_opts:
        if opt in ctx.lemmas:
            retrieve(ctx.lemmas[opt], opt)
    return resp

def trunc_cols(df, cols=None, maxlen=15):
    if cols is None:
        cols=['children', 'features']
    for col in cols:
        df[col] = df[col].apply(lambda x: ', '.join(x)[:maxlen] + "..")
    return df

# print_def=True
print_def=False
print_synsets=True
serial_numbers='❶❷❸❹❺❻❼❽❾❿'
def rs_represent(rs, data, return_df=False):
    import sagas
    from sagas.nlu.rules import verb_patterns, aux_patterns, subj_patterns, predict_patterns
    from sagas.nlu.rules_lang_spec import langspecs
    from sagas.nlu.nlu_cli import NluCli

    df_set = []
    result = []

    for serial, r in enumerate(rs):
        type_name = r['type']
        meta = build_meta(r, data)
        if type_name == 'verb_domains':
            theme = '[verb]'
            tc.info(serial_numbers[serial], theme,
                  # r['lemma'], r['index'],
                  f"{r['word']}/{r['lemma']}, pos: {r['upos']}/{r['xpos']}, idx: {r['index']}",
                  '(%s, %s)' % (r['rel'], r['governor']))
            # meta = {'rel': r['rel'], **common, **data}
            verb_patterns(meta, r['domains'])
        elif type_name == 'aux_domains':
            theme = '[aux]'
            # 'rel': word.dependency_relation, 'governor': word.governor, 'head': dc.text
            delegator = '☇' if not r['delegator'] else '☌'
            tc.info(serial_numbers[serial], theme, r['lemma'], r['rel'], delegator,
                  "%s(%s)" % (r['head'], r['head_pos']))
            # verb_patterns(r['domains'])
            # meta = {'pos': r['head_pos'], 'head': r['head'], **common, **data}
            aux_patterns(meta, r['domains'])
        elif type_name == 'subj_domains':
            theme = '[subj]'
            tc.info(serial_numbers[serial], theme, r['lemma'], r['rel'], '☇',
                  "%s(%s)" % (r['head'], ', '.join(r['head_feats'])))
            # verb_patterns(r['domains'])
            # meta = {'pos': r['head_pos'], 'head': r['head'], **common, **data}
            subj_patterns(meta, r['domains'])
        elif type_name=='predicate':
            theme = '[predicates]'
            tc.info(serial_numbers[serial], theme,
                  f"{r['lemma']} ({r['phonetic']}, {r['word']})")
            # meta = {'rel': r['rel'], **common, **data}
            predict_patterns(meta, r['domains'])
        elif type_name == 'root_domains':
            theme = '[root]'
            tc.info(serial_numbers[serial], theme,
                  f"{r['word']}/{r['lemma']}, pos: {r['upos']}/{r['xpos']}, idx: {r['index']}",
                  '(%s, %s)' % (r['rel'], r['governor']))
            # meta = {'rel': r['rel'], **common, **data}
            # verb_patterns(meta, r['domains'])
            # check_langspec(data['lang'], meta, r['domains'], type_name)
        else:
            # meta = {}
            raise Exception('Cannot process specific type: {}'.format(type_name))

        # process language special rules
        logger.debug(f"meta keys {meta.keys()}")
        langspecs.check_langspec(data['lang'], meta, r['domains'], type_name)

        # df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'children', 'features'])
        df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
        df_set.append(df)

        if not return_df:

            result.extend(proc_word(type_name, r['word'],
                                    r['head'] if 'head' in r else '',
                                    data['lang']))
            result.extend(proc_children_column(df['rel'], df['children'], data['lang']))

            # print('.......')
            # where 1 is the axis number (0 for rows and 1 for columns.)
            # df = df.drop('children', 1)
            # df['children'] = df['children'].apply(lambda x: ', '.join(x)[:15] + "..")
            # df['features'] = df['features'].apply(lambda x: ', '.join(x)[:15] + "..")
            trunc_cols(df)
            tc.dfs(df)
            print_stem_chunks(r)

            if print_def:
                NluCli().get_word_def(r['lemma'], data['lang'])
            if print_synsets:
                r = display_synsets(theme, meta, r, data['lang'])
                result.extend(r)

    return result, df_set

# target_lang=lambda s: 'zh' if s=='en' else 'en'
target_lang=lambda s: cf.optional('assist_lang', 'zh') if s=='en' else 'en'
def translit_chunk(chunk, lang):
    from sagas.nlu.transliterations import translits
    # if lang in ('ko', 'ja', 'fa', 'hi', 'ar'):
    if translits.is_available_lang(lang):
        return '/'+translits.translit(chunk, lang)
    return ''

def proc_word(type_name, word, head, lang):
    from sagas.nlu.google_translator import translate
    res, _ = translate(word, source=lang, target=target_lang(lang),
                       trans_verbose=False)
    target=''
    if head!='':
        res_t, _ = translate(head, source=lang, target=target_lang(lang),
                           trans_verbose=False, options={'disable_correct'})
        target=f" ⊙︿⊙ {res_t}({head})"
    result=f"[{type_name}]({word}{translit_chunk(word, lang)}) {res}{target}"
    tc.emp('magenta', result)
    return [result]

def proc_children_column(partcol, textcol, lang, indent='\t'):
    from sagas.nlu.google_translator import translate
    result=[]
    # print(partcol, textcol)
    for id, (name, r) in enumerate(zip(partcol, textcol)):
        if name not in ('punct', 'head_root'):
        # if len(r)>1:
            # sent=' '.join(r) if lang not in ('ja','zh') else ''.join(r)
            sent=join_text(r, lang)
            res, _ = translate(sent, source=lang, target=target_lang(lang),
                               trans_verbose=False, options={'disable_correct'})
            chunk=f"{indent}[{name}]({sent}{translit_chunk(sent, lang)}) {res}"
            result.append(chunk)
            tc.emp('cyan', chunk)
    return result

def get_verb_domains(data, return_df=False):
    # import requests
    # from sagas.conf.conf import cf

    if 'engine' not in data:
        data['engine']=cf.engine(data['lang'])
    engine=data['engine']
    response = requests.post(f'{cf.servant(engine)}/verb_domains', json=data)
    # print(response.status_code, response.json())

    if response.status_code == 200:
        rs = response.json()
        result, df_set=rs_represent(rs, data, return_df)

        if return_df:
            return df_set
        else:
            # print(result)
            return result
    return []

class TransContext(object):
    def __init__(self, s,t,q,says,deps):
        self.target_sents = []
        self.sents_map = {}

        self.source=s
        self.targets=t
        self.text=q
        self.says=says
        self.deps=deps

    def pars(self):
        return self.source, self.targets, self.text, self.says

    @property
    def target_list(self):
        rs= self.targets.split(';')
        rs.extend([l for l in self.deps.split(';') if l not in rs and l!=''])
        return rs

class MiscTool(object):
    def __init__(self):
        import sagas.conf.conf as conf
        # import logging
        # import os

        cf = conf.TransClipConf()
        self.translator=cf.conf['translator']
        self.retries=cf.conf['retries']
        self.enable_chunks_parse=cf.conf['enable_chunks_parse']
        self.enable_ascii_viz = cf.conf['enable_ascii_viz']
        self.append_ascii_viz=cf.conf['append_ascii_viz']
        print('.. default translator - %s, retries times - %d, enable chunks parse - %s'
              %(self.translator, self.retries, self.enable_chunks_parse))
        self.translators={'baidu':self.trans_baidu,
                          'google':self.trans_google}

        # logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    def plain(self):
        """
        $ python -m sagas.tool.misc plain
        :return:
        """
        import clipboard
        text = clipboard.paste()
        text = text.replace("\n", "")
        # print(text)
        clipboard.copy(text)
        return text

    def plain_sents(self):
        """
        $ python -m sagas.tool.misc plain
        :return:
        """
        import clipboard
        text = clipboard.paste()
        text = text.replace("\n", "")
        text = f"\t('{text}', ''),"
        clipboard.copy(text)
        return text

    def add_serial_no(self):
        """
        $ python -m sagas.tool.misc add_serial_no
        :return:
        """
        import clipboard
        text = clipboard.paste()
        begin = 1
        result = []
        for line in text.splitlines():
            result.append(str(begin) + ". " + line)
            begin = begin + 1
        clipboard.copy("\n".join(result))

    def wrap_sent(self):
        """
        $ python -m sagas.tool.misc wrap_sent
        :return:
        """
        import clipboard
        text = clipboard.paste()
        text = "'%s', "%(text.replace("\n", ""))
        clipboard.copy(text)
        return text

    def trans_google(self, ctx:TransContext):
        from tqdm import tqdm
        from sagas.nlu.google_translator import translate
        import time
        import random
        source, targets, text, says=ctx.pars()

        # for target in tqdm(targets.split(';')):
        print('.. translate to', ctx.target_list)
        for target in tqdm(ctx.target_list):
            options=set()
            # default options
            options.add('disable_correct')
            if says==target:
                options.add('get_pronounce')
            if says==source and target=='en':
                options.add('get_pronounce')

            trans, tracker=translate(text, source=source, target=target, options=options)
            count = 0
            while trans=='':
                print('wait a second, try again ...')
                sleep(1)
                trans, tracker = translate(text, source=source, target=target, options=options)
                count=count+1
                if count>self.retries:
                    break

            if trans != '':
                # result=text+'\n\t* '+trans+'\n'
                # line='[%s] '%target[:2]+trans
                line = '%s="%s"' % (target[:2], trans)
                ctx.target_sents.append(line)
                # ctx.target_sents.extend(tracker.pronounce)
                for i,p in enumerate(tracker.pronounce):
                    ps=p[2:]
                    ctx.target_sents.append(f'v{i}="{ps}"')
                ctx.sents_map[target[:2]]=trans
                # print('☌'+line)
            else:
                print('translate fail, the clipboard content has not been changed.')
                # will exit
                return False

            time.sleep(random.uniform(0.05, 0.20))

        return True

    def trans_baidu(self, ctx: TransContext):
        from tqdm import tqdm
        from sagas.nlu.baidu_translator import BaiduTranslator
        import time

        tr=BaiduTranslator()
        # for t in tqdm(ctx.targets.split(';')):
        for t in tqdm(ctx.target_list):
            result=tr.trans(ctx.source, t, ctx.text)
            # print(result)
            if len(result)==0:
                print(f'** Cannot translate text from {ctx.source} to {t}: {ctx.text}')
                break

            trans=result[0]['dst']
            line = '%s="%s"' % (t[:2], trans)
            ctx.target_sents.append(line)
            ctx.sents_map[t[:2]] = trans

            time.sleep(1.0)  # must wait 1 second
        return True

    def trans_clip_opt(self, source):
        """
        $ python -m sagas.tool.misc trans_clip_opt de
        :param source:
        :return:
        """
        self.translator='baidu' # set this option
        print('.. set translator', self.translator)
        if source=='ja':
            targets='en;zh'
        else:
            targets='zh;ja'
        self.trans_clip(source, targets=targets, says='ja', details=False)

    def parse_chunks(self, text, source, targets, ctx, details=True):
        import sagas.nlu.corenlp_helper as helper
        from sagas.nlu.treebanks import treebanks

        def query_serv(data, print_it=True):
            response = requests.post(f'{cf.servant_by_lang(data["lang"])}/digest', json=data)
            # print(response.status_code, response.json())
            if response.status_code == 200:
                ctx.target_sents.append(response.text)

                if print_it:
                    result= response.json()
                    print_terms(data['sents'], result)
        def query_serv_zh(data, print_it=True):
            response = requests.post('http://localhost:8091/digest', json=data)
            if response.status_code == 200:
                ctx.target_sents.append(response.text)

                if print_it:
                    result= response.json()
                    print_terms_zh(data['sents'], result)

        # available_sources=['en', 'de', 'fr', 'ru', 'es', 'it', 'pt', 'cs', 'sk', 'pl', 'tr',
        #                    'sv', 'no', 'hi']
        available_sources=set(list(helper.langs.keys())+treebanks.support_langs)
        if details:
            if source in available_sources:
                data = {'lang': source, "sents": text}
                query_serv(data)

            # common targets
            if 'en' in targets:
                data = {'lang': 'en', "sents": ctx.sents_map['en']}
                query_serv(data)
            if 'ja' in targets:
                data = {'lang': 'ja', "sents": ctx.sents_map['ja']}
                query_serv(data)
            if 'zh' in targets:
                data = {'lang': 'zh', "sents": ctx.sents_map['zh']}
                query_serv_zh(data)

        result='\n\t'.join([text]+ctx.target_sents)
        print(result)

        addons=[]

        # print('??????? ......')
        # if False:
        if source in available_sources:
            data = {'lang': source, "sents": text}
            # if source=='zh':
            #     data['engine']='ltp'
            # else:
            #     data['engine']='corenlp'
            data['engine']=cf.engine(source)
            addons.extend(get_verb_domains(data))
        elif 'en' in ctx.sents_map:
            # there is no available dep-parser for the source language,
            # use english instead of it
            data = {'lang': 'en', "sents": ctx.sents_map['en']}
            addons.extend(get_verb_domains(data))

        if details:
            if 'ja' in targets:
                data = {'lang': 'ja', "sents": ctx.sents_map['ja']}
                get_verb_domains(data)

        return addons, result

    def trans_en_to(self, text, lang, translit_targets=None, said=True):
        import clipboard
        from sagas.nlu.transliterations import translits

        source = 'en'
        targets = f'fr;zh-CN;{lang}'
        says = lang
        # details=False

        ctx = TransContext(source, targets, text, says, '')
        ctx.sents_map[source[:2]] = text
        succ = self.translators[self.translator](ctx)
        if not succ:
            return

        # addons, result = self.parse_chunks(text, source, targets, ctx, details=details)
        addons = []
        # result = '\n\t'.join([text] + ctx.target_sents)
        lines = []
        lines.append(f'\t.sent({source}="{text}"')
        suffix = ") \\"
        # other appendants like: ctx.target_sents.append(f'v{i}="{ps}"')

        # add translits
        if translit_targets is not None:
            for i, translit in enumerate(translit_targets):
                ps=translits.translit(ctx.sents_map[translit], translit)
                ctx.target_sents.append(f't{i}="{ps}"')

        result = ', \n\t      '.join(lines + ctx.target_sents + [suffix])
        print(result)

        clipboard.copy(result)

        if said:
            from sagas.nlu.nlu_tools import NluTools
            NluTools().say(ctx.sents_map[says], says)

    def trans_en_ar(self, *args):
        """
        $ python -m sagas.tool.misc trans_en_ar please repeat.
        :param args:
        :return:
        """
        self.trans_en_to(merge_args(args), 'ar', ['ar'])

    def trans_en_ko(self, *args):
        self.trans_en_to(merge_args(args), 'ko', ['ko'])
    def trans_en_fa(self, *args):
        self.trans_en_to(merge_args(args), 'fa', ['fa'], said=False)
    def trans_en_hi(self, *args):
        self.trans_en_to(merge_args(args), 'hi', ['hi'], said=True)
    def trans_en_he(self, *args):
        self.trans_en_to(merge_args(args), 'he', ['he'], said=True)
    def trans_en_fi(self, *args):
        self.trans_en_to(merge_args(args), 'fi', ['fi'], said=True)
    def trans_en_pt(self, *args):
        self.trans_en_to(merge_args(args), 'pt', ['pt'], said=True)

    def trans_clip(self, source='auto', targets='zh-CN;ja',
                   says=None, details=True, sents='', deps=''):
        """
        $ trans
        $ trans auto en
        $ trans ru en
        $ trans ru 'zh-CN;ja'
        $ trans-ru
        $ trans-rus

        $ alias sp="python -m sagas.tool.misc trans_clip pt 'en;it;ja' ja False"
        $ sp 'O homem fica amarelo.'
        $ sa 'أنا متأسف.'
        $ sf "La similitude entre ces deux phrases" 'ja;zh;id'
        $ sz '这两句话的相似程度' en
        $ sz '这两句话的相似程度' 'en;fr;ar;ja;fa'
        $ engine=spacy se 'I like to eat cucumber.'
        $ sj '足にひどい痛みを感じました。'  # multiple predicates

        :return:
        """
        import clipboard
        from sagas.nlu.nlu_cli import NluCli

        ascii_incompatibles=['zh', 'ja', 'ko', 'ar', 'fa']

        if sents!='':
            text=sents
            interact_mode=False
        else:
            text = clipboard.paste()
            text = text.replace("\n", "")
            interact_mode=True

        # remove spaces if lang is ja/zh
        # if source in ('ja','zh'):
        #     text=text.replace(' ','')
        text=fix_sents(text, source)
        engine=cf.engine(source)
        tc.emp('yellow', f".. parse with {engine}: ({text})")
        # add at 2019.9.15
        ascii_gs=[]
        if self.enable_ascii_viz:
            rt=NluCli().ascii_viz(text, source, engine=engine)
            if source not in ascii_incompatibles:
                ascii_gs.extend(rt.split('\n'))
            print(rt)
        # target_sents=[]
        # sents_map={}
        ctx=TransContext(source, targets, text, says, deps)
        # print('❣', text)
        if source!='auto':
            # text = fix_sents(source, text)
            ctx.sents_map[source[:2]] = text

        # addi_pronounce=[]
        # succ=self.trans_google(ctx)
        succ=self.translators[self.translator](ctx)

        if not succ:
            return
        # if len(addi_pronounce)>0:
        #     target_sents.extend(addi_pronounce)

        ## addons
        if self.enable_chunks_parse:
            addons, result = self.parse_chunks(text, source, targets, ctx, details=details)
        else:
            addons=[]
            # result = '\n\t'.join([text] + ctx.target_sents)
            lines=[]
            lines.append(f'\t.sent({source}="{text}"')
            suffix=") \\"
            result = ', \n\t      '.join(lines + ctx.target_sents+[suffix])
            print(result)

        # other langs dep-parse
        if self.enable_ascii_viz and deps!='':
            for t in deps.split(';'):
                if t in ctx.sents_map:
                    rt=NluCli().ascii_viz(ctx.sents_map[t], t, engine=cf.engine(t))
                    # ascii_gs.extend(rt.split('\n'))
                    print(rt)
                else:
                    color_print('red', f".. the lang {t} for dep-parse is not available in translated list.")

        if interact_mode:
            result = result + '\n\t'
            if self.append_ascii_viz and len(ascii_gs)>0:
                result=result+'\n\t'.join(ascii_gs)

            if len(addons)>0:
                # result=result+'\n\t'+'\n\t'.join(addons)
                result = result + '\n\t'.join(addons)
            if self.enable_chunks_parse:
                result=result+'\n'
            # clipboard.copy(result+'\n')
            clipboard.copy(result)

        if interact_mode and says is not None:
            from sagas.nlu.nlu_tools import NluTools
            NluTools().say(ctx.sents_map[says], says)

    def verb_domains(self, sents, lang='en', engine='corenlp'):
        """
        $ python -m sagas.tool.misc verb_domains 'Мы написали три книги за год.' ru
        $ python -m sagas.tool.misc verb_domains 'Ivan is the best dancer .' en
        $ python -m sagas.tool.misc verb_domains 'Ivan is the best dancer .' en spacy
        $ domains 'Die Aufnahmen begannen im November.' de
        $ domains '伊万是最好的舞者' zh ltp
        $ domains '现在是几点' zh ltp
        $ domains '现在是几点?' zh corenlp
        :param sents:
        :param lang:
        :return:
        """
        data = {'lang': lang, "sents": sents, 'engine':engine}
        get_verb_domains(data)

    def dep_parse(self, sents, lang='en', engine='corenlp'):
        """
        $ python -m sagas.tool.misc dep_parse 'Мы написали три книги за год.' ru
        $ python -m sagas.tool.misc dep_parse "今何時ですか?" ja
        $ python -m sagas.tool.misc dep_parse "今何時ですか?" ja knp
        $ python -m sagas.tool.misc dep_parse "私の趣味は、多くの小旅行をすることです。" ja knp
        $ python -m sagas.tool.misc dep_parse "自由を手に入れる" ja
        $ python -m sagas.tool.misc dep_parse "现在是几点?" zh ltp
        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        from sagas.nlu.uni_jsonifier import rs_summary
        from sagas.nlu.corenlp_parser import get_chunks
        from sagas.nlu.uni_remote import dep_parse

        doc_jsonify, resp = dep_parse(sents, lang, engine, ['predicts'])
        rs = get_chunks(doc_jsonify)
        rs_summary(rs)
        print('-' * 25, 'predicts')
        pprint(resp)
        print('-' * 25, 'doc')
        pprint(doc_jsonify.as_json)

    def exec_rules(self, sents, lang='en', engine='corenlp'):
        """
        $ python -m sagas.tool.misc exec_rules "今何時ですか?" ja
        $ python -m sagas.tool.misc exec_rules "今何時ですか?" ja knp
        $ python -m sagas.tool.misc exec_rules "望遠鏡で泳いでいる少女を見た。" ja knp
        $ python -m sagas.tool.misc exec_rules 'Мы написали три книги за год.' ru
        $ python -m sagas.tool.misc exec_rules "现在是几点?" zh ltp
        $ rules '我在臺灣開計程車。' zh
        $ rules '我在台湾开出租车。' zh ltp
        $ rules "吸烟对你的健康有害。" zh ltp
        $ rules 'Tini berumur sepuluh tahun.' id
        $ rules 'Berapa umur kamu?' id  (因为找不到预定义的chunks模式, 所以会输出所有单词和依赖关系)

        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        from sagas.nlu.corenlp_parser import get_chunks
        from sagas.nlu.uni_remote import dep_parse

        pipelines=['predicts']
        doc_jsonify, resp = dep_parse(sents, lang, engine, pipelines)
        if doc_jsonify is not None:
            color_print('cyan', resp)
            if len(resp['predicts'])>0:
                rs_represent(resp['predicts'], data = {'lang': lang, "sents": sents, 'engine': engine,
                                     'pipelines':pipelines})
            else:
                rs = get_chunks(doc_jsonify)
                if len(rs)>0:
                    # rs_summary(rs)
                    rs_represent(rs, data = {'lang': lang, "sents": sents, 'engine': engine,
                                             'pipelines':pipelines})
                else:
                    color_print('red', '.. no found predefined chunk-patterns.')
                    print(doc_jsonify.words_string())
                    print(doc_jsonify.dependencies_string())

if __name__ == '__main__':
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    fire.Fire(MiscTool)
