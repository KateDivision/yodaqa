#!/bin/bash
# This script is not intended to be run separately
# Always call from label-lookup.sh or sqlite.sh
# Download data
#wget http://www-nlp.stanford.edu/pubs/crosswikis-data.tar.bz2/dictionary.bz2
wget https://nlp.stanford.edu/data/crosswikis-data.tar.bz2/lnrm.dict.bz2

# Preprocess data
#./sqlite-init.py labels.db dictionary.bz2
./sqlite-init.py labels.db lnrm.dict.bz2
