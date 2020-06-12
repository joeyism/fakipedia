#!/bin/bash
export MODEL_DIR=fakipedia_distil
export GPT2_TYPE=distilgpt2
export DATA_FOLDER=wikitext-2-raw
export TRAIN_FILE=$DATA_FOLDER/wiki.eot.train.raw 
export EVAL_FILE=$DATA_FOLDER/wiki.test.raw 

python run_language_modeling.py \
--output_dir=$MODEL_DIR \
--model_type=$GPT2_TYPE \
--model_name_or_path=$GPT2_TYPE \
--do_train \
--train_data_file=$TRAIN_FILE \
--do_eval \
--eval_data_file=$EVAL_FILE \
--save_steps=-1 \
--per_gpu_train_batch_size=2 \
--num_train_epochs=5

tar -czf $MODEL_DIR.tar.gz $MODEL_DIR
