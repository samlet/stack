import json
import json_utils

def convert_list(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def load_assocs():
    import json_utils
    data=json_utils.read_json_file("./data/corpus/mondly_assocs.json")
    return data

def load_verbs():
    import json_utils
    data=json_utils.read_json_file("./data/corpus/mondly_verbs.json")
    return {k:set(v) for k,v in data.items()}

class MondlyCorpus(object):
    def __init__(self):
        self.all_assocs = load_assocs()
        self.verb_assocs=load_verbs()

    def launch_driver(self):
        import time
        from selenium import webdriver
        self.driver = webdriver.Chrome(
            '/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.
        self.driver.get('https://app.mondly.com/home')

    def shutdown(self):
        self.driver.quit()

    def put_assoc(self, key_s, value_s):
        if key_s in self.all_assocs:
            value_ls = self.all_assocs[key_s]
            if value_s in value_ls:
                return False
            else:
                value_ls.append(value_s)
        else:
            self.all_assocs[key_s] = [value_s]
        return True

    def put_assocs(self, assocs):
        # the key is target language, value is english(will be as key)
        for k, v in assocs.items():
            if k != '' and v != '':
                self.put_assoc(v, k)

    def extract_assocs(self):
        nums = self.driver.find_elements_by_class_name("words")
        # print(f"total sections {len(nums)}")
        texts = []
        for el in nums:
            # print(el.text)
            lines=el.text.split('\n')
            if (len(lines) % 2) != 0:
                lines = lines[1:]
            texts.extend(lines)
        print(f"total sents {len(texts)}")
        texts_count = len(texts)
        if (texts_count % 2) != 0:
            texts = texts[1:]
        text_assocs = convert_list(texts)
        print(f"current assocs {len(text_assocs)}")
        # for k,v in text_assocs.items():
        #     print(f"{k} -> {v}")
        json_s = json.dumps(text_assocs, indent=2, ensure_ascii=False)
        # print(json_s)
        self.put_assocs(text_assocs)
        print(f"total assocs {len(self.all_assocs)}")
        # print(json.dumps(self.all_assocs, indent=2, ensure_ascii=False))
        json_utils.write_json_to_file("./data/corpus/mondly_assocs.json",
                                      self.all_assocs)

    def put_verb(self, text):
        if ' = ' in text:
            pair = text.split(' = ')
            key = pair[1]
            val = pair[0]
            if key in self.verb_assocs:
                self.verb_assocs[key].add(val)
            else:
                self.verb_assocs[key] = {val}
            return True
        return False

    def extract_verbs(self):
        import json_utils
        verbs = self.driver.find_elements_by_class_name("translation-verb")
        # print('total section', len(verbs))
        for v in verbs:
            # print(v.text)
            for t in v.text.split('\n'):
                self.put_verb(t)
        # print(verb_assocs)
        # print(jsonpickle.encode(verb_assocs))
        json_data = {k: list(v) for k, v in self.verb_assocs.items()}
        print(f"total verbs {len(self.verb_assocs)}")
        # print(json.dumps(json_data,
        #                 indent=2, ensure_ascii=False))
        json_utils.write_json_to_file("./data/corpus/mondly_verbs.json", json_data)

if __name__ == '__main__':
    import fire
    fire.Fire(MondlyCorpus)

