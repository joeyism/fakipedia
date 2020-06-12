#!/bin/bash
# setup instance
sudo apt -y install unzip

#git clone https://github.com/NVIDIA/apex apex
#cd $_
#pip3 install -v --no-cache-dir ./
#cd -

pip3 install --user -r requirements.txt
pip3 install --user -r requirements-dev.txt

# get data
## WikiText-2
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-raw-v1.zip
unzip wikitext-2-raw-v1.zip
python3 -m scripts.add_eot_to_file wikitext-2-raw/wiki.train.raw

## WikiText-103
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-raw-v1.zip
unzip wikitext-103-raw-v1.zip
python3 -m scripts.add_eot_to_file wikitext-103-raw/wiki.train.raw

# train
bash scripts/train.sh
