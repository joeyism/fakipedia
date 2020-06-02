#!/bin/bash

MODEL_DIR=fakipedia_model_med
GPT2_TYPE=gpt2-medium


# setup instance
sudo apt -y install unzip
git clone https://github.com/NVIDIA/apex /tmp
cd $_
pip3 install -v --no-cache-dir ./
cd -
pip3 install --user -r requirements.txt
pip3 install --user -r requirements-dev.txt

# get data
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-raw-v1.zip
unzip wikitext-2-raw-v1.zip

python run_language_modeling.py \
--output_dir=$MODEL_DIR \
--model_type=$GPT2_TYPE \
--model_name_or_path=$GPT2_TYPE \
--do_train \
--train_data_file=wikitext-2-raw/wiki.train.raw \
--do_eval \
--eval_data_file=wikitext-2-raw/wiki.valid.raw \
--save_steps=-1 \
--per_gpu_train_batch_size=1 \
--num_train_epochs=5

tar -czf $MODEL_DIR.tar.gz $MODEL_DIR