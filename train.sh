#!/bin/bash
mkdir -p ./rasa-app-data/projects
mkdir -p ./rasa-app-data/logs

python -m rasa_nlu.train \
    --config ./config/config.yml \
    --data nlu_data/ \
    --path ./rasa-app-data/projects \
    --project french

# -o PATH, --path PATH  Path where model files will be saved
