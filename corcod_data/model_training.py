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
        for d in data:
            print()
            labels.append(d[14])
        # labels = [d[len(d)-1] for d in ls]
        ls = [int(i) for i in ls]
        print(labels[200])
        print(ls[200])


read_data('metadata.csv')