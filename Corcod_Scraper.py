#Scraping a csv file from a website and tokenizing it using NLP

import nltk
#nltk.download('punkt') #uncomment this line if you are running this for the first time
#nltk.download('stopwords') #uncomment this line if you are running this for the first time


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#Reading the file
import pandas as pd
import numpy as np

#Reading the file
csv_data = open('corcod_data/metadata.csv')
csv_data = pd.read_csv(csv_data)

#data_point = np.array([(csv_data[i].file_name, csv_data[i].complexity) for i in range(1,2)])
#print(data_point)

data_points = np.array((csv_data.file_name, csv_data.complexity))
print(data_points[0][1])

#java_code = java_code.read()


java_code = open('corcod_data/Dataset/' + data_points[0][1])
java_code = java_code.read()
#print(java_code)


words = word_tokenize(java_code)
#print(words)

stop_words = set(stopwords.words("english"))
added_stop_words = ["{","}",
                    "(",")",";","=","<",">","[","]",".",",","/","*","&","%","$","#","@","!","?","|","\"","\'","\\","`","~","^","-","+","_","0","1","2","3","4","5","6","7","8","9"]

print(stop_words)

filtered_sentence = [w for w in words if not w in stop_words]

#print(filtered_sentence)

    
"""

filtered_sentence = []

for w in words:
    if w not in stop_words:
        filtered_sentence.append(w)

print(filtered_sentence)

filtered_sentence = [w for w in words if not w in stop_words]

print(filtered_sentence)

filtered_sentence = []

for w in words:
    if w not in stop_words:
        filtered_sentence.append(w)

print(filtered_sentence)

filtered_sentence = [w for w in words if not w in stop_words]

print(filtered_sentence)

filtered_sentence = []

for w in words:
    if w not in stop_words:
        filtered_sentence.append(w)

print(filtered_sentence)

filtered_sentence = [w for w in words if not w in stop_words]

print(filtered_sentence)

filtered_sentence = []

for w in words:
    if w not in stop_words:
        filtered_sentence.append(w)

print(filtered_sentence)

filtered_sentence = [w for w in words if not w in stop_words]

print(filtered_sentence)

filtered_sentence = []

for w in words:
    if w not in stop_words:
        filtered_sentence.append(w)

print(filtered_sentence)

filtered_sentence = [w for w in words if not w in stop_words]

print(filtered_sentence)

filtered_sentence = []

for w in words:
    if w not in stop_words:
        filtered_sentence.append(w)

print(filtered_sentence)
"""


