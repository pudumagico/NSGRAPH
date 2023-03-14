#!/bin/sh
echo "SMALL" &
python main.py clevr-graph/small
echo "MEDIUM" &
python main.py clevr-graph/medium
echo "LARGE" &
python main.py clevr-graph/large