
data = [1,2,3,4,5]


def graph():
    print(data)
    for i in range(len(data)-1):
        data[i] = data[i+1]
    data[-1] = data[-2] +1

for i in range(10): 
    graph()
  