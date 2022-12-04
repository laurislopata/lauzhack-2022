def read_data(filename):
    with open(filename, 'r') as f:
        data = f.read()
        data = data.split('\n')
        ls = []
        for d in data:
            datapoint = d.split(',')
            ls.append(datapoint[:len(datapoint)-1])
        labels = []
        print(len(ls[200]))
        for d in ls:
            if len(d) < 15:
                continue
            labels.append(d[14])
        
        for i in range(len(ls) - 2):
            if len(ls[i]) < 15:
                del ls[i]
        
        # labels = [d[len(d)-1] for d in ls]
        X = []
        for i in ls:
            X.append(i[:len(i)-1])
        
        # Convert X from string to int
        X = X[1:]

        for i in range(len(X)):
            for j in range(len(X[i])):
                X[i][j] = int(X[i][j])
        
        return X, labels


X, str_y = read_data('metadata.csv')

Y = []

for s in str_y:
    if s == '1':
        Y.append(1)
    elif s == 'logn':
        Y.append(2)
    elif s == 'n':
        Y.append(3)
    elif s == 'nlogn':
        Y.append(4)
    elif s == 'n_square':
        Y.append(5)

# print(X[1:5])
# print(Y[1:5])

del X[784]
del Y[784]

# for index, x in enumerate(X):
#     if len(x) != 14:
#         print(index)
#         print(x)

import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))


def train_model(X, y):
    # print(np.array(X).shape)
    # print(np.array(y).shape)
    clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
    clf.fit(X, y)
    return clf

X = X[1:]
model = train_model(X, Y)
# tst = np.array(X[1]).reshape(-1, 1)
# print(tst)
print(model.predict([X[170]]))

predictions = model.predict(X)