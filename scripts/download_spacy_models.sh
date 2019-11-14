#!/bin/bash
array=( en es fr de el nb lt nl pt it )
for i in "${array[@]}"
do
    echo "$i ..."
    python -m spacy download ${i}_core_news_sm
done

python -m spacy validate
