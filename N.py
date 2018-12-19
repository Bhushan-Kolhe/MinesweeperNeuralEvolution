import numpy as np

class NeuralNetwork:
    def __init__(self,Dimnemsions):
        self.Dimensions = Dimnemsions
        self.Parameters = {}
        self.initializeParameters()
        self.cache_A = {}
        self.cache_Z = {}
        self.cost = 0
        self.LearningRate = 0.05
        self.grads = {}
        self.DesiredOutput = 0
        #print(self.Parameters)

    def initializeParameters(self):
        for i in range(1,len(self.Dimensions)):
            self.Parameters['W' + str(i)] = np.random.randn(self.Dimensions[i], self.Dimensions[i-1]) * 0.01
            self.Parameters['b' + str(i)] = np.zeros(shape=(self.Dimensions[i], 1))

    def feedForward(self):
        for i in range(1,len(self.Dimensions)):
            W1 = self.Parameters['W' + str(i)]
            b = self.Parameters['b' + str(i)]
            A0 = self.cache_A['A' + str(i-1)]
            Z = np.dot(W1, A0) + b
            self.cache_Z['Z' + str(i)] = Z
            self .cache_A['A' + str(i)] = self.activation(Z)
    
    def activation(self,Z):
        A = (np.exp(Z) - np.exp(-Z))/(np.exp(Z)+np.exp(-Z))
        return A
    
    def inputFuncTrain(self,x,y):
        self.cache_A['A0'] = x
        self.DesiredOutput = y
        self.feedForward()
        self.computeCost(self.cache_A['A' + str(len(self.Dimensions)-1)], self.DesiredOutput)
        self.feedBackward(self.cache_A['A' + str(len(self.Dimensions)-1)], self.DesiredOutput)
        self.updateParameters()

    def inputFuncTest(self,x):
        self.cache_A['A0'] = x
        self.feedForward()
        return self.getOutput()
        
    def getOutput(self):
        return self.cache_A['A' + str(len(self.Dimensions)-1)]

    def computeCost(self,O,D):
        self.cost = 0.5*((D-O)**2)
    
    def activationBackward(self,Z):
        return (1 - self.activation(Z)**2)

    def feedBackward(self,O,D):
        l = len(self.Dimensions)
        dZ_prev = (O-D)*self.activationBackward(self.cache_Z['Z' + str(l-1)])
        for i in range(1,len(self.Dimensions)):
            dW = dZ_prev * self.cache_A['A' + str(l-i-1)].T
            db = np.sum(dZ_prev, axis=1, keepdims=True)
            if l-1-i != 0:
                dZ_prev = (np.dot(self.Parameters['W' + str(l-i)].T,dZ_prev))*self.activationBackward(self.cache_Z['Z' + str(l-1-i)])
            self.grads['dW' + str(l-i)] = dW
            self.grads['db' + str(l-i)] = db

    def updateParameters(self):
        for i in range(1,len(self.Dimensions)):
            self.Parameters['W' + str(i)] = self.Parameters['W' + str(i)] - self.LearningRate * self.grads['dW' + str(i)]
            self.Parameters['b' + str(i)] = self.Parameters['b' + str(i)] - self.LearningRate * self.grads['db' + str(i)]

    def setParameters(self, Params):
        self.Parameters = Params

    def getParameters(self):
        return self.Parameters



#NN = NeuralNetwork([100,64,64,200])
#NN2 = NeuralNetwork([100,64,64,200])
#print(NN.getParameters())