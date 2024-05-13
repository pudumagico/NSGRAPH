# NSGRAPH

Repository of the code used in the paper 
A Modular Neurosymbolic Approach for Visual Graph Question Answering, submitted to the ICLP 2024 conference.

## Abstract
> Images containing graph-based structures are an ubiquitous and popular form of data representation that, to the best of our knowledge, have not yet been considered in the domain of Visual Question Answering (VQA). We use CLEGR, a graph question answering dataset with a generator that synthetically produces vertex-labelled graphs that are inspired by metro networks. Additional information about stations and lines is provided, and the task is to answer natural language questions concerning such graphs. While symbolic methods suffice to solve this dataset, we consider the more challenging problem of taking images of the graphs instead of their symbolic representations as input. Our solution takes the form of a modular neurosymbolic model that combines the use of optical graph recognition for graph parsing, a pretrained optical character recognition neural network for parsing node labels, and answer-set programming, a popular logic-based approach to declarative problem solving, for reasoning. The implementation of the model achieves an overall average accuracy of 73\% on the dataset, providing further evidence of the potential of modular neurosymbolic systems in solving complex VQA tasks, in particular, the use and control of pretrained models in this architecture.

## Enviroment Set Up
You may install the whole enviroment by using the command:
```
conda env create -f environment.yml -n NSGRAPH
conda activate NSGRAPH
```

## Reproducing Experiments
To reproduce the numbers presented in the paper, please download the data used from [here](https://drive.google.com/file/d/1IwKL55rmh5r8pBNLNo1IRBjT5J9YCbqo/view?usp=share_link).
Then, use the following command to execute the inference process over the data
```
python main.py -fp <path_to_data_folder>
python main.py -fp <path_to_data_folder> -ocrgt True
python main.py -fp <path_to_data_folder> -ogrgt True
```
The first command uses the system without access to any ground truth, the second uses ground truth labels and the third uses ground truth about nodes, edges and lines. 
