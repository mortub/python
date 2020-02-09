# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 07:30:49 2018

@author: Mor Tubul   id:311420418
"""
import numpy as np
import os
import matplotlib.pyplot as plt


#calculates the value of the tour 
def computeTourLength(perm, Graph) :
    tlen = 0.0
    for i in range(len(perm)) :
        tlen += Graph[perm[i],perm[np.mod(i+1,len(perm))]]
    return tlen
#calculates the tour
def computeTour(perm, Graph) :
     tour=[]
     for i in range(len(perm)) :
        tour.append( Graph[perm[i],perm[np.mod(i+1,len(perm))]])
     return tour

def simmulatedAnnealing() :
    #the range in which the indices are neighbours
    LOWBOUNDNEIGHBOUR=-2
    HIGHBOUNDNEIGBOUR=2
    #reading from the file the graph
    dirname = ""
    fname = os.path.join(dirname,"hachula130.dat.txt")
    data = []
    NTrials = 10#**5
    with open(fname) as f :
        for line in f:
            data.append(line.split())
    n = len(data)
    G = np.empty([n,n])
    #creating the graph
    for i in range(n) :
        for j in range(i,n) :
            G[i,j] = np.linalg.norm(np.array([float(data[i][1]),float(data[i][2])]) - np.array([float(data[j][1]),float(data[j][2])]))
            G[j,i] = G[i,j]
    T_init=40.0
    T_min=1e-5
    alpha=0.999
    max_internal_runs = 50
    local_state = np.random.RandomState(seed=None)
    eval_cntr = 1
    T = T_init
    #a variable to make sure we run until NTrials
    eval_cntr = 1
    #a random number of coordinates that will be changed into their neighbours
    rand_for_loop=(np.random.randint(1, HIGHBOUNDNEIGBOUR+1))
    #the minimal permutation, starts randomly
    minPerm=np.random.permutation(n)  
    #saves the minimal tour in the whole run
    bestTour=[]
    #saves all of the values of all tours in the run
    tourStat = []
    #saves the minimal value tour in the whole run
    fbest=computeTourLength(minPerm,G)
    #while we havn't reaches the minimal temprature and havn't reached NTrials trials
    while ((T >= T_min) and eval_cntr < NTrials ) :
        #for each trial do max_internal_runs times
        for _ in range(max_internal_runs) :
            #copying the minPerm into newPerm
            newPerm=minPerm
            #chooses one random number in the range
            neigbourRange=(np.random.randint(LOWBOUNDNEIGHBOUR,HIGHBOUNDNEIGBOUR+1))
            eval_cntr += 1
            #choosing random indices to change in the new permutation
            for i in range(rand_for_loop):
                #choosing a random index of the permutation to add a neighbour to
                rand=(np.random.randint(0, n))
                #making sure that the indices are between 1-n
                neighbour=newPerm[rand]+neigbourRange;
                if neighbour > 0 and  neighbour < n:
                    newPerm[rand]=neighbour
            #after altering the newPerm, see if there is an improvement
            delta=computeTourLength(newPerm,G)-computeTourLength(minPerm,G)
            #if the newPerm gives me a smaller/ same length of tour
            #or if the probability stands, change the minimal perm to the new one
            if delta <= 0 or local_state.uniform(size=1) < np.exp(-delta/T):
                minPerm=newPerm 
            #if there is a better result, save it in the best result
            value=computeTourLength(newPerm,G)
            if value <  fbest :           
                fbest=value
                bestTour=computeTour(newPerm, G)
                    
            tourStat.append(value)
        T *= alpha
            
    plt.hist(tourStat,bins=100)
    plt.show()
   
    return fbest,bestTour
    
if __name__ == "__main__" :
    bestLength=0.0
    bestTour=[]
    tempBestLength=0.0
    tempBestTour=[]
    # a starting best length+tour
    bestLength,bestTour=simmulatedAnnealing()
    max_runs=30
    for _ in range(max_runs-1) :
        tempBestLength,tempBestTour=simmulatedAnnealing()
        if tempBestLength < bestLength:
            bestLength=tempBestLength
            bestTour=tempBestTour
    
    print(bestTour)
    print(bestLength)
    
    
    