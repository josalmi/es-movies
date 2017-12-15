#!/bin/bash
set -e
./et index create 0
./et index alias movies 0
curl http://elasticsearch:9200/_aliases
python import-movies.py
