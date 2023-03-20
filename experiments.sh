#!/bin/sh
echo "SMALL" 
python main.py -fp clevr-graph/small
echo "SMALL OCR GT" 
python main.py -fp clevr-graph/small -ocrgt True
echo "SMALL OGR GT" 
python main.py -fp clevr-graph/small -ogrgt True
echo "MEDIUM" 
python main.py -fp clevr-graph/medium
echo "MEDIUM OCR GT" 
python main.py -fp clevr-graph/medium -ocrgt True
echo "MEDIUM OGR GT" 
python main.py -fp clevr-graph/medium -ogrgt True
echo "LARGE" 
python main.py -fp clevr-graph/large
echo "LARGE OCR GT" 
python main.py -fp clevr-graph/large -ocrgt True
echo "LARGE OGR GT" 
python main.py -fp clevr-graph/large -ogrgt True