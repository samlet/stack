#!/bin/bash
python -m sagas.graph.graph_manager create_lang_feeds it /pi/ai/seq2seq/ita-eng/ita.txt ./data/graph/ita_eng_feed.json
python -m sagas.graph.graph_manager create_lang_feeds pt /pi/ai/seq2seq/por-eng/por.txt ./data/graph/por_eng_feed.json

