# procs-rasa-issues.md
1. 非内部的component, 名称只能是全路径, 否则无法在配置文件中对其进行配置:
    + workspace/rasa/stack/sagas/provider/time_extractor.py
        name = "sagas.provider.time_extractor.TimeExtractor"
        