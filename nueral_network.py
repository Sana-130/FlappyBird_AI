import numpy as np
import random

class NueralNetwork():
    def __init__(self, n_inputs, n_nueron, n_output):
        self.n_inputs = n_inputs
        self.n_nueron = n_nueron
        self.n_output = n_output
        self.h_weights =  np.random.randn(n_inputs, n_nueron)
        self.o_weights =  np.random.randn(n_nueron, n_output)
        self.h_biases = np.random.randn(1, n_nueron)
        self.o_biases = np.random.randn(1, n_output)

    def feedforward(self, inputs):
        output_1 = np.dot(inputs, self.h_weights) + self.h_biases
        h_o = self.activation(output_1)
        output_2 = np.dot(h_o, self.o_weights) + self.o_biases
        h2_o = self.activation(output_2)
        return h2_o

    def activation(self, inputs):
        #sigmoid activation function
        return (1 / (1 + np.exp(-inputs)))

    def crossover(self , wi, wo, wi_2, wo_2, bi, bo, bi_2, bo_2):
        
        single_point = round(self.n_inputs/2)
        matrix = np.zeros((self.n_inputs, self.n_nueron))
        matrix[0 : single_point, 0: self.n_nueron] = wi[0 : single_point, 0: self.n_nueron]
        matrix[single_point : self.n_inputs, 0: self.n_nueron]=wi_2[single_point : self.n_inputs, 0: self.n_nueron]

        self.h_weights=matrix
        

        single_point = round(self.n_nueron/2)
        matrix = np.zeros((1, self.n_nueron))
        matrix[0:1, 0:single_point] = bi[0:1, 0:single_point]
        matrix[0:1 , single_point: self.n_nueron] = bi_2[0:1 , single_point: self.n_nueron]

        self.h_biases = matrix
        #print(self.h_biases)

        matrix = np.zeros((self.n_nueron, self.n_output))
        single_point = random.randint(0 , round(self.n_nueron/2))
        matrix[0 : single_point, 0:self.n_output] = wo[0 : single_point, 0:self.n_output]
        matrix[single_point : self.n_nueron, 0: self.n_output]=wo_2[single_point : self.n_nueron, 0: self.n_output]

        self.o_weights=matrix

        matrix = np.zeros((1, self.n_output))
        #rand= random.randint(0,1)
        #if rand:
        #    matrix[0][0] = bo[0][0]
        #else:
        #    matrix[0][0] = bo_2[0][0]
        matrix[0][0]=min(bo[0][0], bo_2[0][0]) 
        
        #matrix[0:1, single_point:self.n_output] = bo_2[0:1, single_point:self.n_output]
        
        self.o_biases = matrix  

    def mutate(self, rate):
        for i in range(self.n_inputs):
            if rate > random.uniform(0 , 1):
                for j in range(self.n_nueron):
                #r=random.randint(0, self.n_inputs-1)
                #t=random.randint(0, self.n_nueron-1)
                #self.h_weights[r][t] += 0.5 * random.uniform(0,1) #0.5 * random.uniform(0,1)                
                #self.o_weights[t][0] += 0.5 *random.uniform(0,1) #0.5 * random.uniform(0,1)
                    self.h_weights[i][j] += random.uniform(-1, 1)
                    pass
        for i in range(self.n_nueron):
            if rate > random.uniform(0 , 1):
                for j in range(self.n_output): 
                    self.o_weights[i][j] += random.uniform(-1, 1) 
                    pass
        for i in range(1):
            if rate > random.uniform(0 , 1):
                for j in range(self.n_nueron): 
                    self.h_biases[i][j] += random.uniform(-1, 1)
                    pass
        for i in range(1):
            if rate > random.uniform(0 , 1):
                for j in range(self.n_output): 
                    self.o_biases[i][j] += random.uniform(-1, 1)  
                    pass
        
        pass