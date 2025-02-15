import numpy as np


def perceptron(data, labels, params = {}, hook = None):    
    T = params.get('T', 100)
    d, n = data.shape
    theta = np.zeros(d)
    theta_0 = np.zeros(1)

    counter = 0

    for t in range(T):
        for i in range(n):
            if labels.T[i] * (theta.T.dot(data.T[i]) + theta_0) <= 0:
                theta = theta + labels.T[i] * data.T[i]
                theta_0 = theta_0 + labels.T[i]
                counter = counter + 1
                

    print("Try: " + str(counter))
    return(np.array([theta]).T, np.array([theta_0]))


data1c = np.array([[200, 800, 200, 800], [0.2,  0.2,  0.8,  0.8]])
labels1 = np.array([[-1, -1, 1, 1]])

data1h = np.array([[0.2, 0.8, 0.2, 0.8], [0.2,  0.2,  0.8,  0.8]])

data2a = np.array([[2, 3,  4,  5]])
labels2a = np.array([[1, 1, -1, -1]])

print(perceptron(data2a, labels2a, params={'T':100}))