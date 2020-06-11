#!/bin/bash
export MODEL_DIR=fakipedia_distil
export GPT2_TYPE=distilgpt2


# setup instance
sudo apt -y install unzip
git clone https://github.com/NVIDIA/apex apex
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
--fp16 \
--fp16_opt_level=O2 \
--save_steps=-1 \
--per_gpu_train_batch_size=4 \
--num_train_epochs=3

tar -czf $MODEL_DIR.tar.gz $MODEL_DIR
