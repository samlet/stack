#!/bin/bash
python -m sagas.graph.graph_manager create_lang_feeds
python -m sagas.graph.graph_manager create_lang_feeds ja /pi/ai/seq2seq/jpn-eng-2019/jpn.txt ./data/graph/jpn_eng_feed.json
python -m sagas.graph.graph_manager create_lang_feeds zh /pi/ai/seq2seq/cmn-eng-2019/cmn.txt ./data/graph/cmn_eng_feed.json True
python -m sagas.graph.graph_manager create_lang_feeds de /pi/ai/seq2seq/deu-eng/deu.txt ./data/graph/deu_eng_feed.json
python -m sagas.graph.graph_manager create_lang_feeds es /pi/ai/seq2seq/spa-eng/spa.txt ./data/graph/spa_eng_feed.json

