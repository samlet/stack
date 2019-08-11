#!/bin/bash
bert-serving-start -model_dir /pi/ai/bert/uncased_L-12_H-768_A-12/ -num_worker=2 -max_seq_len=50


