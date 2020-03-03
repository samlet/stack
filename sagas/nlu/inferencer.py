import requests
from sagas.conf.conf import cf
from sagas.nlu.rules_meta import build_meta
from sagas.nlu.rules_lang_spec import langspecs
from sagas.nlu.sinkers import Sinkers
from sagas.startup import startup
from sagas.tool import init_logger
from sagas.tool.misc import translit_chunk, display_synsets
import sagas.tracker_fn as tc
from sagas.nlu.utils import fix_sents, join_text
import sagas
from pprint import pprint

# def fix_data(data):
#     if 'engine' not in data:
#         data['engine'] = cf.engine(data['lang'])
#     data['sents']=fix_sents(data['sents'], data['lang'])
#     return data

def parse(data):
    if 'engine' not in data:
        data['engine']=cf.engine(data['lang'])
    engine=data['engine']
    response = requests.post(f'{cf.servant(engine)}/verb_domains', json=data)
    if response.status_code == 200:
        return response.json()
    return None

def proc_word(type_name, word, head, index, lang):
    from sagas.nlu.google_translator import translate
    res, _ = translate(word, source=lang, target=target_lang(lang),
                       trans_verbose=False)

    # result=f"[{type_name}]({word}{translit_chunk(word, lang)}) {res}{target}"
    result = {'type': type_name, 'text': word,
              'translit': translit_chunk(word, lang),
              'translate': res,
              'lang': lang,
              'index': index,
              }
    if head != '':
        res_t, _ = translate(head, source=lang, target=target_lang(lang),
                             trans_verbose=False, options={'disable_correct'})
        # target=f" ⊙︿⊙ {res_t}({head})"
        result['head'] = head
        result['head_trans'] = res_t
    # tc.emp('magenta', result)
    return result


target_lang = lambda s: cf.optional('assist_lang', 'zh') if s == 'en' else 'en'


# def proc_children_column(partcol, textcol, idxcol, lang):
def proc_children_column(df, lang):
    from sagas.nlu.google_translator import translate
    result = []
    # for id, (name, r) in enumerate(zip(partcol, textcol)):
    rels = []
    for id, row in df.iterrows():
        # df['rel'], df['children'], df['index']
        name, r, idx = row['rel'], row['children'], row['index']
        if name in rels:
            continue
        else:
            rels.append(name)
        if name not in ('punct', 'head_root'):
            sent = join_text(r, lang)
            res, _ = translate(sent, source=lang, target=target_lang(lang),
                               trans_verbose=False, options={'disable_correct'})
            # chunk=f"{indent}[{name}]({sent}{translit_chunk(sent, lang)}) {res}"
            chunk = {'name': name, 'text': sent,
                     'translit': translit_chunk(sent, lang),
                     'translate': res,
                     'index': idx,
                     }
            result.append(chunk)
            # tc.emp('cyan', chunk)
    return result


def induce_spec(el, pats, type_name):
    # print(f"{el.indicator} {el.word}: {el.spec}")
    if el.indicator == '[verb]':
        pats.append((3, f"behaveof('{el.spec}', 'v')"))
    elif el.indicator == '[aux]':
        # pats.append((3, f"behaveof('{el.spec}', '*')"))
        pass
    elif el.indicator == '[root]':
        pats.append((3, f"behaveof('{el.spec}', 'n')"))
    elif el.indicator == '[predicate]':
        pats.append((3, f"specsof('*', '{el.spec}')"))
    else:
        if type_name in ('aux_domains', 'subj_domains') and el.indicator == 'head':
            pats.append((3, f"behaveof('{el.spec}', '*')"))
        else:
            pats.append((1, f"{el.indicator}=kindof('{el.spec}', '*')"))


def induce_part(chunk, pats, type_name, enable_verbose = False):
    if enable_verbose:
        tc.emp('cyan', chunk)
    gen_map = {'nsubj': lambda: (2, "nsubj=agency"),
               'advmod': lambda: (4, "extract_for('plain', 'advmod')"),
               'cop': lambda: (2, "cop='c_aux'"),
               'head_amod': lambda: (2, "head_amod=interr('what')"),
               '時間': lambda: (4, "extract_for('plain+date_search+date_parse', '時間')"),
               }
    if chunk.name in gen_map:
        pats.append(gen_map[chunk.name]())


def induce_pattern(pat, ds, enable_verbose = False):
    if enable_verbose:
        tc.emp('magenta', pat)

    def gen_verb(ind='verb', prefix='behave'):
        spec = [d for d in ds if d['indicator'] == f'[{ind}]']
        if spec:
            ref = spec[0]['spec']
        else:
            ref = pat.translate.replace(' ', '_')
        return f"pat(5, name='{prefix}_{ref}').verb"

    def gen_root():
        spec = [d for d in ds if d['indicator'] == '[root]']
        if spec:
            ref = spec[0]['spec']
        else:
            ref = pat.translate.replace(' ', '_')
        return f"pat(5, name='ana_{ref}').root"

    def gen_cop():
        spec = [d for d in ds if d['indicator'] == 'head']
        if spec:
            ref = spec[0]['spec']
        else:
            ref = pat.head_trans.replace(' ', '_') if pat.lang != 'en' else pat.head.replace(' ', '_')
        return f"pat(5, name='desc_{ref}').cop"

    domap = {'verb_domains': gen_verb,
             'aux_domains': gen_cop,
             'subj_domains': gen_cop,
             'root_domains': gen_root,
             'predicate': lambda: gen_verb('predicate', 'predict'),
             }
    return domap[pat.type]()

class Inferencer(object):
    def infer(self, sents, lang, verbose=False):
        """
        $ python -m sagas.nlu.inferencer infer '水としょうゆを混ぜた。' ja
            pat(5, name='predict_mix').verb(specsof('*', 'mix'), ヲ=kindof('water', '*')),
        $ python -m sagas.nlu.inferencer infer 'Ellos ya leyeron ese libro en la escuela.' es
            pat(5, name='behave_read').verb(extract_for('plain', 'advmod'), behaveof('read', 'v'), nsubj=agency, obl=kindof('school', '*'), obj=kindof('book', '*')),
        $ python -m sagas.nlu.inferencer infer 'you are dead' en
            pat(5, name='desc_dead').cop(behaveof('dead', '*'), nsubj=agency, cop='c_aux'),
        $ python -m sagas.nlu.inferencer infer '予約を火曜日から木曜日に変えてもらった。' ja
        $ python -m sagas.nlu.inferencer infer ''太陽は月に比べて大きいです。' ja
        $ python -m sagas.nlu.inferencer infer 'Berapa umur kamu?' id # (en="How old are you?")
            pat(5, name='ana_age').root(behaveof('age', 'n')),
        $ python -m sagas.nlu.inferencer infer 'Apa yang lebih murah?' id # (What is cheaper?)
            pat(5, name='desc_abundant').cop(extract_for('plain', 'advmod'), behaveof('abundant', '*'), nsubj=agency, head_amod=interr('what')),

        :param sents:
        :param lang:
        :return:
        """
        data = {'lang': lang, "sents": sents}
        rs = parse(data)
        result_pats=[]
        # sinkers = Sinkers()
        for serial, r in enumerate(rs):
            type_name = r['type']
            theme = type_name.split('_')[0]
            # print(type_name)
            meta = build_meta(r, data)
            # print(f"meta keys {meta.keys()}")

            # mod_rs = langspecs.check_langspec(data['lang'], meta, r['domains'], type_name)
            # sinkers.add_module_results(mod_rs)

            # infers
            pats = []

            def do_infers(ds):
                df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])

                pat = proc_word(type_name, r['word'],
                                r['head'] if 'head' in r else '',
                                r['index'],
                                data['lang'])
                pat_r = induce_pattern(sagas.to_obj(pat), ds, verbose)
                parts = proc_children_column(df, data['lang'])
                for part in parts:
                    induce_part(sagas.to_obj(part), pats, type_name, verbose)
                # display_synsets(f"[{theme}]", meta, r, data['lang'])
                return pat_r

            # induce with wordnet
            ds = display_synsets(f"[{theme}]", meta, r, data['lang'], collect=True)
            pat_r = do_infers(ds)
            indicators = []
            for el in ds:
                if el['indicator'] not in indicators:
                    induce_spec(sagas.to_obj(el), pats, type_name)
                    indicators.append(el['indicator'])

            pats = sorted(pats, key=lambda pat: -pat[0])
            paras = ', '.join(p[1] for p in pats)
            result_pats.append(f"{pat_r}({paras}),")

            # debug
            if verbose:
                print('*', '-' * 45)
                pprint(ds)

        # sinkers.process_with_sinkers()
        return result_pats

infers=Inferencer()

if __name__ == '__main__':
    import fire
    init_logger()
    # startup.start()
    fire.Fire(Inferencer)