#!/bin/sh
echo "SMALL" 
python main.py -fp clevr-graph/small
echo "MEDIUM" 
python main.py -fp clevr-graph/medium
echo "LARGE" 
python main.py -fp clevr-graph/large