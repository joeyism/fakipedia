#!/bin/bash

MODEL_DIR=fakipedia_model_med
GPT2_TYPE=gpt2-medium

# setup instance
sudo apt -y install unzip

# get data
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-raw-v1.zip
unzip wikitext-2-raw-v1.zip

python run_language_modeling.py \
--output_dir=$MODEL_DIR \
--model_type=$GPT2_TYPE \
--model_name_or_path=$GPT2_TYPE \
--do_train \
--train_data_file=wikitext-2-raw/wiki.train.raw \
--eval_data_file=wikitext-2-raw/wiki.valid.raw \
--per_gpu_train_batch_size=2 \
--num_train_epochs=5
