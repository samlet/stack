import json_utils
import pandas as pd
import json
import re

def norm_key(s):
    s = re.sub(r"[^a-zA-Z]+", r"", s)
    return s[:4].lower()

def process_ru_cols(row, cols_list):
    rs=set([])
    for col in cols_list:
        if pd.notnull(row[col]):
            rs.update(row[col].lower().replace("'",'').split(';'))
    return list(rs)

def add_to(rs_df, all_dicts, cols_list):
    for index, row in rs_df.iterrows():
        if pd.notnull(row['translations_en']):
            ru_word=row['bare']
            en_words=row['translations_en'].lower().split(', ')
            if pd.notnull(row['translations_de']):
                de_words=row['translations_de'].split(', ')
            else:
                de_words=[]
            all_dicts.append({'en':en_words,
                              'ru':process_ru_cols(row, cols_list),
                              'de':de_words
                             })
def print_json(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))

def filter_set(all_dicts, ru_word_set, lang='ru', absents=None):
    from tqdm import tqdm
    rs=[]
    for word in tqdm(ru_word_set):
        word=word.lower()
        find_it=False
        for item in all_dicts:
            if word in item[lang]:
                rs.append(item)
                find_it=True
        if absents is not None and not find_it:
            absents.append(word)
    return rs

def build_dicts():
    all_dicts = []
    cols = 'bare	partner	imperative_sg	imperative_pl	past_m	past_f	past_n	past_pl	presfut_sg1	presfut_sg2	presfut_sg3	presfut_pl1	presfut_pl2	presfut_pl3'
    cols_list = cols.split('\t')
    # dict_maps={'v':'verbs', 'n':'nouns', 'a':'adjectives', 'o':'others'}
    dict_maps = {'verbs': cols_list,
                 'nouns': 'bare	partner	sg_nom	sg_gen	sg_dat	sg_acc	sg_inst	sg_prep	pl_nom	pl_gen	pl_dat	pl_acc	pl_inst	pl_prep'.split(
                     '\t'),
                 'adjectives': 'bare	comparative	superlative	short_m	short_f	short_n	short_pl	decl_m_nom	decl_m_gen	decl_m_dat	decl_m_acc	decl_m_inst	decl_m_prep	decl_f_nom	decl_f_gen	decl_f_dat	decl_f_acc	decl_f_inst	decl_f_prep	decl_n_nom	decl_n_gen	decl_n_dat	decl_n_acc	decl_n_inst	decl_n_prep	decl_pl_nom	decl_pl_gen	decl_pl_dat	decl_pl_acc	decl_pl_inst	decl_pl_prep'.split(
                     '\t'),
                 'others': 'bare'.split('\t'),
                 }
    for dict_name, cols in dict_maps.items():
        verbs = '/pi/nlp/russian-dictionary/%s.csv' % dict_name
        print('process', verbs)
        df = pd.read_csv(verbs, delimiter='\t')
        add_to(df, all_dicts, cols)
    print('total words', len(all_dicts))
    return all_dicts

def build_voc():
    voc_file='/pi/langs/voc/ru-voc.json'
    voc_dicts='/pi/langs/voc/ru-voc-dicts.json'
    words=json_utils.read_json_file(voc_file)
    all_dicts=build_dicts()

    print('filter by voc-words ...')
    skips=[]
    rs=filter_set(all_dicts, words, 'ru', skips)
    json_utils.write_json_to_file(voc_dicts, rs)
    # print('done.')
    print('absents %d, see these words in file ru-voc-absents.json'%len(skips))
    json_utils.write_json_to_file('/pi/langs/voc/ru-voc-absents.json', skips)

    return rs, skips

def build_input_pairs(additions):
    import clipboard

    voc_dicts = '/pi/langs/voc/ru-voc-dicts.json'
    voc_words = json_utils.read_json_file(voc_dicts)
    print('total voc words', len(voc_words))
    rs = []
    for w in voc_words:
        for en_w in w['en']:
            ru_w = ' '.join(w['ru']).replace(',', '')
            rs.append('%s %s' % (norm_key(en_w), ru_w))
    print('input pairs contains voc words %d, and ips words %d'%(len(rs), len(additions)))
    clipboard.copy('\n'.join(rs+additions))



