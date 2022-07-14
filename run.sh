#!/bin/bash

/usr/bin/curl -s "$1" > docbin_full.json;
/usr/bin/curl -s "$2" > labeling_functions.py;
/usr/bin/curl -s "$3" > knowledge.py;
/usr/local/bin/python run_lf.py "$4" "$5" "$6";
