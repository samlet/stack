def list_ru_files(dir):
    suffix='.md'
    prefix='ru-'
    import os
    rs=[]
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(suffix) and file.startswith(prefix):
                rs.append(os.path.join(root, file))
    return rs

voc='''а,a
б,b
в,v
г,ɡ
д,d
е,e
ё,o
ж,ʒ
з,z
и,i
й,j
к,k
л,l
м,m
н,n
о,o
п,p
р,r
с,s
т,t
у,u
ф,f
х,x
ц,t͡s
ч,t͡ɕ
ш,ʂ
щ,ɕɕ
ъ,
ы,ɨ
ь,ʲ
э,e
ю,u
я,a
дж,d͡ʒ'''

class RuProcs(object):
    def __init__(self):
        import epitran
        print(".. load rus-Cyrl")
        self.epi = epitran.Epitran('rus-Cyrl')

        self.target_file = '/pi/langs/voc/ru-map.json'
        self.target_file_rev = '/pi/langs/voc/ru-rev-map.json'

    def get_phonetic(self, argument):
        """
        >>> print(epi.transliterate(u'Вот оно что'))
        $ python -m sagas.ru.ru_procs get_phonetic 'Вот оно что'
        :param argument:
        :return:
        """
        result = self.epi.transliterate(argument)
        return result

    def get_files(self):
        files=list_ru_files('/pi/langs')
        return files

    def get_all_words(self, get_ref_lines=False):
        import re
        all_words = set([])
        discard_file = 'ru-todos.md'
        files=self.get_files()
        files = [f for f in files if not f.endswith(discard_file)]
        sentences = []
        for filename in files:
            with open(filename) as f:
                lines = f.readlines()
                for line in lines:
                    # only get lines which no leading spaces
                    if line.startswith(' '):
                        continue
                    line = line.strip()
                    if len(line) == 0 or line.startswith('#'):
                        continue
                    sentences.append(line)
                    line = re.sub(r"([,.!?«»\"])", r"", line)
                    all_words.update(line.split(' '))

        discard_set = ['', '–', '-', ',', '.']
        all_words.symmetric_difference_update(x for x in all_words if x in discard_set)
        all_words.symmetric_difference_update(x for x in all_words if x.isdigit())
        if get_ref_lines:
            return all_words, sentences
        return all_words

    def save_voc(self):
        import json_utils
        all_words=self.get_all_words()
        json_utils.write_json_to_file('/pi/langs/voc/ru-voc.json', list(all_words))

    def get_norm_key(self, word, verbose=False, truncate=4):
        ipa_xs = self.epi.xsampa_list(word)
        if verbose:
            print('❣', word, ipa_xs)
        key = ''.join(ipa_xs).replace('\\', '') \
                  .replace('s`', 'sh').replace("'", '') \
                  .replace('1', 'y').lower()[:truncate]
        return key

    def print_chars(self):
        """
        $ python -m sagas.ru.ru_procs print_chars
        :return:
        """
        for v in voc.split('\n'):
            pair = v.split(',')
            print(pair[0], pair[1], '\t', self.epi.xsampa_list(pair[0]))

    def ips(self, word):
        """
        $ python -m sagas.ru.ru_procs ips мальчик
        :param word:
        :return:
        """
        ipa_xs = self.epi.xsampa_list(word)
        ipa = self.epi.transliterate(word)
        print(word, ipa, '☌', ''.join(ipa_xs), self.get_norm_key(word))

    def build_words_map(self, to_clip=True):
        """
        $ python -m sagas.ru.ru_procs build_words_map
        $ build-ru
        :param to_clip:
        :return:
        """
        import clipboard
        import json_utils
        words_map = {}
        rev_map = {}
        rs = []
        all_words=self.get_all_words()
        for word in all_words:
            key = self.get_norm_key(word)
            if len(key) > 0:
                if key in words_map:
                    words_map[key].append(word)
                else:
                    words_map[key] = [word]
                rev_map[word] = key
                rs.append('%s %s' % (key, word))

        print('write to', self.target_file)
        json_utils.write_json_to_file(self.target_file, words_map)
        json_utils.write_json_to_file(self.target_file_rev, rev_map)
        if to_clip:
            print('copy to clipboard ...')
            clipboard.copy('\n'.join(rs))
        print('done')

    def build_inputs(self, rebuild=False):
        """
        $ python -m sagas.ru.ru_procs build_inputs
        :return:
        """
        from sagas.ru.ru_comparisons import build_voc, build_input_pairs

        if rebuild:
            print('collecting words ...')
            self.save_voc()
            print('rebuilding voc file ...')
            # _, skips=build_voc()
            build_voc()

        all_words=self.get_all_words()
        print('building input-method resources ...')
        addons=[]
        for word in all_words:
            key = self.get_norm_key(word)
            if len(key) > 0:
                addons.append('%s %s' % (key, word))

        print('merge output ...')
        build_input_pairs(addons)
        print('done.')

    def word_info(self, word):
        """
        $ python -m sagas.ru.ru_procs word_info мальчик
        :param word:
        :return:
        """
        import json_utils

        ipa_xs = self.epi.xsampa_list(word)
        ipa = self.epi.transliterate(word)

        rev_map=json_utils.read_json_file(self.target_file_rev)
        words_map=json_utils.read_json_file(self.target_file)
        key = rev_map[word]
        print(word, ipa, ''.join(ipa_xs), '☌', key)
        print('\t', words_map[key])

    def word_info_df(self, word):
        import sagas
        import json_utils
        rev_map = json_utils.read_json_file(self.target_file_rev)
        words_map = json_utils.read_json_file(self.target_file)

        tuples = []
        ipa_xs = self.epi.xsampa_list(word)
        ipa = self.epi.transliterate(word)
        key = rev_map[word]
        tuples.append((word, ipa, ''.join(ipa_xs), key))
        for w in words_map[key]:
            ipa_xs = self.epi.xsampa_list(w)
            ipa = self.epi.transliterate(w)
            tuples.append((w, ipa, ''.join(ipa_xs), key))
        return sagas.to_df(tuples, ['word', 'ipa', 'xsampa_list', 'key'])

    def ref_sentences(self, sentences, word):
        rs = []
        for s in sentences:
            if word in s:
                rs.append(s)
        return rs

    def say_refs(self, word, limit=10):
        """
        $ python -m sagas.ru.ru_procs say_refs мальчик
        :param word:
        :return:
        """
        from sagas.nlu.nlu_tools import NluTools
        words, sents=self.get_all_words(True)
        sents = self.ref_sentences(sents, word)
        print('total sentences', len(sents))
        for s in sents[:limit]:
            print(s)
            NluTools().say(s, 'ru')

    def about(self, word):
        """
        $ python -m sagas.ru.ru_procs about мальчик
        $ about мальчик
        :param word:
        :return:
        """
        print(self.word_info_df(word))

    def lookup(self, pos, word_pat, enable_de=True):
        """
        Search dictionary by English word
        $ python -m sagas.ru.ru_procs lookup v search
        $ python -m sagas.ru.ru_procs lookup n 'bird|fish'
        $ python -m sagas.ru.ru_procs lookup n 'bird|fish' False
        $ lookup n bear
        :param pos: will be one of n/v/a/o
        :param word_pat:
        :return:
        """
        from sagas.ru.ru_dictionary import RuDictionary
        print('.. load dictionary')
        dic=RuDictionary(pos=pos)
        rs=dic.lookup(word_pat, enable_de)
        print(rs)

if __name__ == '__main__':
    import fire
    fire.Fire(RuProcs)
