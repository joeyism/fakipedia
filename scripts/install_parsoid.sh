#!/bin/bash
sudo apt install dirmngr
sudo apt-key advanced --keyserver keys.gnupg.net --recv-keys AF380A3036A03444
sudo apt-add-repository "deb https://releases.wikimedia.org/debian jessie-mediawiki main"

