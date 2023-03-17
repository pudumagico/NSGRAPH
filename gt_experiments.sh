#!/bin/sh
echo "SMALL" 
python main.py -fp clevr-graph/small -ocrgt True
python main.py -fp clevr-graph/small -ogrgt True
echo "MEDIUM" 
python main.py -fp clevr-graph/medium -ocrgt True
python main.py -fp clevr-graph/medium -ogrgt True
echo "LARGE" 
python main.py -fp clevr-graph/large -ocrgt True
python main.py -fp clevr-graph/large -ogrgt True