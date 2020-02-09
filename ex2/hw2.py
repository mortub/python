# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 12:39:42 2018

@author: Mor Tubul id:311420418
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 09:27:05 2018

@author: Mor Tubul id:311420418
"""

import numpy as np
import operator
import random

population_size=1000

def generateChromosome(nQueens):
    #setting an arranged array from 0 to n-1
    init_distribution = np.arange(nQueens)
    #shuffeling a permutation
    np.random.shuffle(init_distribution)
    return init_distribution

def check_clashes(chromosome):
    clashes = 0;
    # calculate row and column clashes
    # just subtract the unique length of array from total length of array
    # [1,1,1,2,2,2] - [1,2] => 4 clashes
    row_col_clashes = abs(len(chromosome)-len(np.unique(chromosome)))
    clashes += row_col_clashes

    # calculate diagonal clashes
    for i in range(len(chromosome)):
        for j in range(len(chromosome)):
            if ( i != j):
                dx = abs(i-j)
                dy = abs(chromosome[i] - chromosome[j])
                if(dx == dy):
                    clashes += 1
    return clashes
#the function is responsible for the cross over: c1 and c2 are chromosomes
def cross_over(c1,c2,nQueens,seed=None):
    local_state = np.random.RandomState(seed)
    idx = local_state.randint(nQueens,dtype=int)
    Xnew1 = np.concatenate((c1[:idx],c2[idx:]))
    Xnew2 = np.concatenate((c2[:idx],c1[idx:]))
    #returning the 2 new chromosomes
    
    return Xnew1,Xnew2
#the function is responsible for the mutation: c1 is a chromosome
def mutation(c1,nQueens,seed=None):
    idx = random.uniform(0, 1)
    if (idx <= 0.8):
        local_state = np.random.RandomState(seed)
        idx = local_state.randint(nQueens,dtype=int)
        if(c1[idx] == (nQueens-1)) :
             c1[idx] = 0
        else :
             c1[idx] += 1
    return c1
def GA(nQueens):
    eval_cntr = 0    
    max_evals=10**4
    #creating a matrix representing the population
    population = np.zeros( (population_size, nQueens))
    population_1 = np.zeros( (population_size, nQueens))
    fitness = np.zeros( (population_size, 2))
    #fill the matrix with random queens locations vectors 
    for i in range(population_size):
        population[i] = generateChromosome(nQueens)
    minimal=population[i]
    min_clash=check_clashes(population[i])
    while (eval_cntr < max_evals) :
        #checking the fitness for each vector
        for i in range(population_size):
            clash=check_clashes(population[i])
            #if there are no clashes, there is a solution that is returned
            if (clash == 0):
                return population[i], eval_cntr
            if(clash<min_clash):
                minimal=population[i]
                min_clash=check_clashes(population[i])
            #the fitness and vector index are kept together
            fitness[i] = (i,clash)       
        #creating a sorted array (according to fitness: the lower the better)
        c = sorted(fitness, key=operator.itemgetter(1))
        #putting the half best vectors in a new matrix       
        for i in range(int(population_size/100)):
            population_1[i] = population[int(c[i][0])]
        j=0
        while j<int(population_size -(population_size/100)-1):
            #doing a cross-over for each couple in the best n/100
            local_state = np.random.RandomState(seed=None)
            rand1 = local_state.randint((population_size/100),dtype=int)
            rand2 = local_state.randint((population_size/100),dtype=int)
            c1,c2=cross_over(population_1[rand1],population_1[rand2],nQueens)        
            j+=1
            i+=1          
            #doing a mutation probability for each of the new vectors after the cross-over
            c1=mutation(c1,nQueens)
            c2=mutation(c2,nQueens) 
            #putting the new vectors in the buttom half of the new matrix
            population_1[i]=c1
            population_1[i+1]=c2 
        #the old generation:population becomes the new one:population_1
        population=population_1
        eval_cntr += 1
        
    return minimal,min_clash,eval_cntr              
    
if __name__ == "__main__" :
    # the number of queens to place on the board
    k=0
    n1=8
    n2=16
    n3=32
    n4=64
    while k<2:
        print(GA(n4))
        k+=1 
            
   