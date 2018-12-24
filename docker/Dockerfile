FROM rasa/rasa_nlu:0.13.8-full
# FROM rasa/rasa_nlu:latest-full

# Add a custom system library (e.g. git)
# RUN apt-get update && \
#     apt-get install -y git

# Add a custom python library (e.g. jupyter)
# RUN pip install --no-cache-dir \
#     jupyter

RUN mkdir -p /data/pkg
ENV DATA_DIR="/data/pkg"
COPY ./fr_core* ${DATA_DIR}/
RUN pip install ${DATA_DIR}/fr_core_news_sm-2.0.0.tar.gz --no-cache-dir > /dev/null \
    && pip install ${DATA_DIR}/fr_core_news_md-2.0.0.tar.gz --no-cache-dir > /dev/null \
    && python -m spacy link fr_core_news_sm fr
