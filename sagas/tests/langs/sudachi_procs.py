import json

from sudachipy import tokenizer
from sudachipy import dictionary
from sudachipy import config
import json

with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
    settings = json.load(f)

print(config.SETTINGFILE)
tokenizer_obj = dictionary.Dictionary(settings).create()

sents='東京都へ行く'
mode = tokenizer.Tokenizer.SplitMode.C
for m in tokenizer_obj.tokenize(mode, sents):
    print(m.dictionary_form(), m.part_of_speech())
