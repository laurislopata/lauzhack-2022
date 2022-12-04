#Scraping a csv file from a website and tokenizing it using ML algorithm


#import nltk
#nltk.download('punkt') #uncomment this line if you are running this for the first time
#nltk.download('stopwords') #uncomment this line if you are running this for the first time


#from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords

#Reading the csv file 
import pandas as pd

import numpy as np

# Removing the comments using regex
import regex as re

# Parsing java code
import javalang

# Creating a graph
from run_time_ML.graph import Graph


#Reading the file
csv_data = open('corcod_data/metadata.csv')
csv_data = pd.read_csv(csv_data)

#data_point = np.array([(csv_data[i].file_name, csv_data[i].complexity) for i in range(1,2)])
#print(data_point)

data_points = np.array((csv_data.file_name, csv_data.complexity))

#java_code = java_code.read()


java_code = open('corcod_data/Dataset/' + '1.java')
java_code = java_code.read()

# Removing the comments from the code
def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

nw_code = remove_comments(java_code)


# Ast module is used to parse the java code
#print(java_code)

def ast_parse(java_code):
    try:
        tree = javalang.parse.parse(java_code)
        return tree
    except:
        return None

def graph_parse(tree):
    try:
        for node in tree:
            
        return graph
    except:
        return None



#Graph2Vec module is used to convert the AST to a graph

from graph2vec import Graph2Vec
import graph2vec.trainer as trainer


g2v = Graph2Vec(vector_dimensions= 1024)

# ML algorithm

graphs = []

for code in data_points:
    graph = Graph()

    java_code = open('corcod_data/Dataset/' + code[0]).read()

    nw_code = remove_comments(java_code)

    ast_code = ast_parse(nw_code)

    graph_code = graph_parse(ast_code)

    graphs.append(graph_code)

g2v.fit()

g2v.train(graph_code)

