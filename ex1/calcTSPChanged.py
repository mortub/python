# -*- coding: utf-8 -*-
"""
@author: ofersh@telhai.ac.il
"""
import numpy as np
import os
import matplotlib.pyplot as plt

def computeTourLength(perm, Graph) :
    tlen = 0.0
    for i in range(len(perm)) :
        tlen += Graph[perm[i],perm[np.mod(i+1,len(perm))]]
    return tlen

def computeTour(perm, Graph) :
     tour=[]
     for i in range(len(perm)) :
        tour.append( Graph[perm[i],perm[np.mod(i+1,len(perm))]])
     return tour
 
def monteCarlo() :
    dirname = ""
    fname = os.path.join(dirname,"hachula130.dat.txt")
    data = []
    NTrials = 10**5
    with open(fname) as f :
        for line in f:
            data.append(line.split())
    n = len(data)
    G = np.empty([n,n])
    for i in range(n) :
        for j in range(i,n) :
            G[i,j] = np.linalg.norm(np.array([float(data[i][1]),float(data[i][2])]) - np.array([float(data[j][1]),float(data[j][2])]))
            G[j,i] = G[i,j]
    newPerm=[]  
    bestTour=[]
    tourStat = []
    bestResult=computeTourLength(np.random.permutation(n),G)
    for k in range(NTrials) :
        newPerm=np.random.permutation(n)
        value=computeTourLength(newPerm,G)
        if value < bestResult :
            bestResult=value
            bestTour=computeTour(newPerm, G)
        tourStat.append(value)
        
    plt.hist(tourStat,bins=100)
    plt.show()
    return bestResult,bestTour

if __name__ == "__main__" :
    bestLength=0.0
    bestTour=[]
    tempBestLength=0.0
    tempBestTour=[]
    # a starting best length+tour
    bestLength,bestTour=monteCarlo()
    max_runs=30
    for _ in range(max_runs-1) :
        tempBestLength,tempBestTour=monteCarlo()
        if tempBestLength < bestLength:
            bestLength=tempBestLength
            bestTour=tempBestTour
    
    print(bestTour)
    print(bestLength)