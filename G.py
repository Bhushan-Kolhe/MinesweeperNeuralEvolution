from N import NeuralNetwork
import numpy as np
import time
import random
import pickle

class GeneticAlgorithm:
    def __init__(self,Game,CreateFile,Size):
        self.Game = Game
        self.Population = []
        self.Size = Size
        self.FitnessScore = []
        self.Dimensions = [100,128,128,128,100]
        self.prev = 0
        self.MutatuionRate = 0.2
        self.Generation = 0
        if CreateFile:
            self.initailizePopulation(False)
            f = open("Objects/Population.Config",'w')
            f.close()
            for i in range(self.Size):
                f = open("Objects/Population.Obj"+str(i),'wb')
                f.close()
        else:
            self.initailizePopulation(True)

    def initailizePopulation(self, LoadFromFile):
        self.FitnessScore = [0 for i in range(self.Size)]
        if LoadFromFile:
            for i in range(self.Size):
                    with open('Objects/Population.Obj'+str(i), 'rb') as config_dictionary_file:
                        self.Population.append(pickle.load(config_dictionary_file))
            f = open("Objects/Population.Config",'r')
            self.Generation = int(f.read())
            f.close()
        else:
            for i in range(self.Size):
                self.Population.append(NeuralNetwork(self.Dimensions))
    
    def findFitness(self):
        for i in range(self.Size):
            while self.Game.isPlaying():
                #print(self.Game.getCurrentTiles())
                Tiles = np.array(self.Game.getCurrentTiles()).reshape(self.Dimensions[0],1)
                Out = self.Population[i].inputFuncTest(Tiles)
                Out = Out.argmax(axis=0)
                if self.prev == Out:
                    break
                #print(Out[0], int(Out[0]/self.Game.BlocksPerRow) + 1, Out[0]%self.Game.BlocksPerRow + 1)
                self.Game.showTile(Out[0], int(Out[0]/self.Game.BlocksPerRow) + 1, Out[0]%self.Game.BlocksPerRow + 1)
                #print(i, self.Game.isPlaying(),self.Game.getScore(),self.Game.getCurrentTiles()[Out[0]])
                self.prev = Out
                #self.Game.canvas.update_idletasks()
                #time.sleep(0.1)
            self.FitnessScore[i] = self.Game.getScore()
            self.Game.resetGame()
        print(self.FitnessScore)


    def selectionCrossoverAndMutation(self):
        NewPopulation = []
        Parrent1Params = {}
        Parrent2Params = {}
        Elite = self.Population[self.FitnessScore.index(max(self.FitnessScore))]
        NewPopulation.append(Elite)
        while len(NewPopulation) < self.Size:
            OffParams = {}
            Parrent1 = random.randint(0,self.Size-1)
            Parrent2 = random.randint(0,self.Size-1)
            while Parrent2 != Parrent1:
                Parrent2 = random.randint(0,self.Size)
            Parrent1 = self.Population[Parrent1]
            Parrent2 = self.Population[Parrent2]
            Parrent1Params = Parrent1.getParameters()
            Parrent2Params = Parrent2.getParameters()
            if random.randint(0,1) == 0:
                OffParams['W1'] = Parrent1Params['W1']
                OffParams['W2'] = Parrent1Params['W2']
                OffParams['W3'] = Parrent2Params['W3']
                OffParams['W4'] = Parrent2Params['W4']
                OffParams['b1'] = Parrent1Params['b1']
                OffParams['b2'] = Parrent1Params['b2']
                OffParams['b3'] = Parrent2Params['b3']
                OffParams['b4'] = Parrent2Params['b4']
            else:
                OffParams['W1'] = Parrent2Params['W1']
                OffParams['W2'] = Parrent2Params['W2']
                OffParams['W3'] = Parrent1Params['W3']
                OffParams['W4'] = Parrent1Params['W4']
                OffParams['b1'] = Parrent2Params['b1']
                OffParams['b2'] = Parrent2Params['b2']
                OffParams['b3'] = Parrent1Params['b3']
                OffParams['b4'] = Parrent1Params['b4']

            ##Mutation
            if random.random() < self.MutatuionRate:
                r = str(random.randint(1,4))
                gene = OffParams['W'+ r]
                gene[random.randint(0,len(gene)-1)] = np.random.randn(gene.shape[1],) * 0.01
                OffParams['W'+ r] = gene

            Offspring = NeuralNetwork(self.Dimensions)
            Offspring.setParameters(OffParams)
            NewPopulation.append(Offspring)

        del Parrent1
        del Parrent2
        #print(self.Population)
        for i in range(self.Size):
            del self.Population[0]
        self.Population = NewPopulation

    def trainNetwork(self):
        while True:
            self.findFitness()
            self.selectionCrossoverAndMutation()
            self.Generation += 1
            print('Gneration: {}'.format(self.Generation))
            if self.Generation % 10 == 0:
                for i in range(self.Size):
                    with open('Objects/Population.Obj'+str(i), 'wb') as config_dictionary_file:
                        pickle.dump(self.Population[i], config_dictionary_file)
                    f = open('Objects/Population.Config','w')
                    f.write(str(self.Generation))
                    f.close()
                if input('Do you want to continue[y/n]:') == 'y':
                    continue
                else:
                    break




        

