#!/bin/bash
username=$(whoami)
# Create directory if does not exist
mkdir /mnt/scrap/users/dopiro/docker/data
cd /mnt/scrap/users/dopiro/docker/data

# Clone repo
git clone https://github.com/brmson/label-lookup.git

cd label-lookup

# Download data
wget http://downloads.dbpedia.org/2014/en/labels_en.nt.bz2
wget http://downloads.dbpedia.org/2014/en/page_ids_en.nt.bz2
wget http://downloads.dbpedia.org/2014/en/redirects_transitive_en.nt.bz2

# Decompress data
bzip2 -dk *.bz2

# Prepare data
./preprocess.py labels_en.nt page_ids_en.nt redirects_transitive_en.nt sorted_list.dat

# Setup Sqlite lookup; disable with comment if not necessary
#/bin/bash /mnt/parsafiler1/vol1/users/dopiro/YodaQA/yodaqa/data/setup/labels/lookup-lite.sh

# Rename directory with data
cd ..
mv label-lookup labels

# Return
cd /

