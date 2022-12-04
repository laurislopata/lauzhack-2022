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

def graph_parse(tree, vector):
    if len(tree.children) > 0:
        for child in tree.children:
            if child:
                for li in child:
                    if li.__class__.__name__ == 'MethodDeclaration':
                        vector["MethodDeclaration"] = vector["MethodDeclaration"] + 1
                    if li.__class__.__name__ == 'IfStatement':
                        vector["IfStatement"] = vector["IfStatement"] + 1
                    if li.__class__.__name__ == 'ForStatement':
                        vector["ForStatement"] = vector["ForStatement"] + 1
                    if li.__class__.__name__ == 'ClassDeclaration':
                        vector["ClassDeclaration"] = vector["ClassDeclaration"] + 1
                    if li.__class__.__name__ == 'WhileStatement':
                        vector["WhileStatement"] = vector["WhileStatement"] + 1
                    if li.__class__.__name__ == 'StatementExpression':
                        vector["StatementExpression"] = vector["StatementExpression"] + 1
                    if li.__class__.__name__ == 'LocalVariableDeclaration':
                        vector["LocalVariableDeclaration"] = vector["LocalVariableDeclaration"] + 1
                    if hasattr(li, 'body'):
                        for node in li.body: 
                            if (not node is None) and (issubclass(type(node), javalang.tree.Statement) or issubclass(type(node), javalang.tree.Expression) or issubclass(type(node), javalang.tree.Declaration)):    
                                left_loop = False
                                if node.__class__.__name__ == 'MethodDeclaration':
                                    vector["MethodDeclaration"] = vector["MethodDeclaration"] + 1
                                if node.__class__.__name__ == 'IfStatement':
                                    vector["IfStatement"] = vector["IfStatement"] + 1
                                if node.__class__.__name__ == 'ForStatement':
                                    vector["ForStatement"] = vector["ForStatement"] + 1
                                    vector["CurrentNestingLevel"] = vector["CurrentNestingLevel"] + 1
                                    if vector["CurrentNestingLevel"] > vector["MaxNestingLevel"]:
                                        vector["MaxNestingLevel"] = vector["CurrentNestingLevel"]
                                    left_loop = True
                                if node.__class__.__name__ == 'ClassDeclaration':
                                    vector["ClassDeclaration"] = vector["ClassDeclaration"] + 1
                                if node.__class__.__name__ == 'WhileStatement':
                                    vector["WhileStatement"] = vector["WhileStatement"] + 1
                                    vector["CurrentNestingLevel"] = vector["CurrentNestingLevel"] + 1
                                    if vector["CurrentNestingLevel"] > vector["MaxNestingLevel"]:
                                        vector["MaxNestingLevel"] = vector["CurrentNestingLevel"]
                                    left_loop = True
                                if node.__class__.__name__ == 'StatementExpression':
                                    vector["StatementExpression"] = vector["StatementExpression"] + 1
                                
                                graph_parse(node, vector)
                                if left_loop: 
                                    vector["CurrentNestingLevel"] = vector["CurrentNestingLevel"] - 1 



#Graph2Vec module is used to convert the AST to a graph

# from graph2vec import Graph2Vec
# import graph2vec.trainer as trainer


# g2v = Graph2Vec(vector_dimensions= 1024)

# ML algorithm

graphs = []

for code in ['1008.java']:
    graph = Graph()
    try: 
        java_code = open('corcod_data/Dataset/' + code ).read()
        nw_code = remove_comments(java_code)

        ast_code = ast_parse(nw_code)
        vect = {"MethodDeclaration": 0, "IfStatement": 0, "ForStatement": 0, 
        "ClassDeclaration": 0, "WhileStatement": 0, "StatementExpression": 0, 
        "LocalVariableDeclaration": 0, "MaxNestingLevel": 0, "CurrentNestingLevel": 0}
        if ast_code is not None:
            graph_code = graph_parse(ast_code, vect)
        print(vect)

        train_model(vect)

        graphs.append(graph_code)
    except: 
        print("file not found")
    
# def train_model(filename):
#     # Read the data
#     data = pd.read_csv(filename)

#     model = LinearRegression()
#     model.fit(X, y)
#     return model


# train_model('corcod_data/metadata.csv')

# g2v.fit()

# g2v.train(graph_code)

