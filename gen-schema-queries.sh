#!/bin/bash
python -m sagas.ofbiz.builder gen-model > sagas/ofbiz/schema_queries_g.py
python -m sagas.ofbiz.mutations_builder > sagas/ofbiz/schema_mutations_g.py


