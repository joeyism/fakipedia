#!/bin/bash
export MODEL_DIR=fakipedia_distil
export GPT2_TYPE=distilgpt2

python run_language_modeling.py \
--output_dir=$MODEL_DIR \
--model_type=$GPT2_TYPE \
--model_name_or_path=$GPT2_TYPE \
--do_train \
--train_data_file=wikitext-2-raw/wiki.train.raw \
--do_eval \
--eval_data_file=wikitext-2-raw/wiki.valid.raw \
--save_steps=-1 \
--per_gpu_train_batch_size=2 \
--num_train_epochs=6

tar -czf $MODEL_DIR.tar.gz $MODEL_DIR
