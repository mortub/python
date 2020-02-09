# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 07:56:14 2019

@author: Mor Tubul id: 311420418

"""
import numpy as np
import random
#pheromones matrix
pheromones=[]
#the array of groups
groups=[]
#the set length of each line
LINE=150
#the max number of lines possible
MAX_LINES=200
#max number of iterations
Niter = 10**2
#number of ants
Nant = 200
#the probability of changing the pheromones
prob=0.95
#defines the best solution for all of the ant colony
def allAnts(pheromones,groups):
    #keeping the best fitness
    bestFitness=0
    #keeping the number of lines of the best fitness
    cnt_lines=MAX_LINES
    #keeping the locations of the groups in the linesof the best solution
    lines=[]
    #keeping the current fitness
    curFitness=0
    #keeping the number of lines of the current fitness
    cnt_linesCur=MAX_LINES
    #keeping the locations of the groups in the lines of the current solution
    linesCur=[]
    for i in range(Nant):
        curFitness,cnt_linesCur,linesCur=oneAnt()
        #if it is a better fitness+ a smaller/ equal number of lines,
        #than change the current best
        if curFitness>bestFitness and cnt_linesCur <= cnt_lines:
            bestFitness=curFitness
            cnt_lines=cnt_linesCur
            lines=linesCur
   
    return bestFitness,cnt_lines,lines
#updates the pheromones matrix according to the best ant in the cycle
def updatePheromones(pheromones,bestFitness):
    for i in range(len(groups)):
        for j in range(len(groups)):
            pheromones[i][j]=prob*pheromones[i][j]+ bestFitness
    return pheromones

#defines the path of one ant    
def oneAnt():
    #counting the lines for each ant
    lines=[]
    #the line that is filled each time with groups
    line=[]
    #counts the number of lines used
    cnt_lines=0
    #counts the number of seats taken in a line
    sum_in_group=0
    #saves the indeces of the groups in one line for a probability check
    indeces_of_groups_in_line=[]    
    the_number_of_seats_taken_in_each_line=[]
    
    #a loop as the number of groups for each ant 
    for i in range(len(groups)):
        #if we have arrived at the end of the line,
        #or there isn't room left, start a new line 
        #and add the current to the lines list
        if sum_in_group == LINE or int(groups[i][0]) > (LINE-sum_in_group):
            lines.append(line)
            line=[]
            the_number_of_seats_taken_in_each_line.append(sum_in_group)
            cnt_lines+=1
            sum_in_group=0
            indeces_of_groups_in_line=[]
        #have the group added to the line according to a probability
        rand=random.uniform(0, 1)
        #only if the probability occured, the group will be added to the line       
        if rand >= calcProbEnterLine(pheromones,sum_in_group,indeces_of_groups_in_line,i,groups):
            sum_in_group+=int(groups[i][0])
            line.append(groups[i])
            indeces_of_groups_in_line.append(i)
    #the function returns the fitness, number of lines and the order of the groups in each line
    return fitness(cnt_lines,the_number_of_seats_taken_in_each_line),cnt_lines,lines
    
#receives the amount of seats taken in the line ,pheromones,
# indeces of other groups in the line, and the current group index
def calcPheromonValue(pheromones,sum_in_group,indeces_of_groups_in_line,i):
   #if line is empty, the value is 1
   if sum_in_group == 0.0:
       return 1
   #otherwise, this calculation:
   else:
       sum_all_pherm_of_groups_in_line=0
       for j in range(len(indeces_of_groups_in_line)):
           sum_all_pherm_of_groups_in_line+=pheromones[i][j]
       return sum_all_pherm_of_groups_in_line/sum_in_group
#calculation of the probability to enter to the line
def calcProbEnterLine(pheromones,sum_in_group,indeces_of_groups_in_line,i,groups):
    sum_sizes_and_pValues_all_groups=0
    for j in range(len(groups)):
        pValue=calcPheromonValue(pheromones,sum_in_group,indeces_of_groups_in_line,j)
        size=int(groups[j][0])
        mult_of_size_and_pValue=size*pValue
        sum_sizes_and_pValues_all_groups+=mult_of_size_and_pValue
    #pValue of just the group itself
    pValueCurGroup=calcPheromonValue(pheromones,sum_in_group,indeces_of_groups_in_line,i)
    
    numerator=pValueCurGroup*int(groups[i][0])
    
    return (numerator/sum_sizes_and_pValues_all_groups)

# calculating the fitness for each ant
def fitness(cnt_lines,the_number_of_seats_taken_in_each_line):
    sum_for_numerator=0
    for i in range(cnt_lines):
       mult=(the_number_of_seats_taken_in_each_line[i]/LINE)**2
       sum_for_numerator+= mult  
    return sum_for_numerator/cnt_lines

if __name__ == "__main__" :
    #opening a file, getting all sizes of groups inside groups
    #they are already sorted
    filename1="rotterdam_120groups.dat.txt"
    filename2="roskilde_250groups.dat.txt"
    with open(filename2) as f :
        for line in f:
            groups.append(line.split())  
    #pheromones matrix
    pheromones= np.zeros((len(groups),len(groups)))
    #init the pheromones matrix with random numbers
    for i in range(len(groups)):
        for j in range(len(groups)):
            rand=random.uniform(0, 1)
            pheromones[i][j]=rand
    
    #keeping the best fitness
    bestFitness=0
    #keeping the number of lines of the best fitness
    cnt_lines=MAX_LINES
    #keeping the locations of the groups in the linesof the best solution
    lines=[]
    #keeping the current fitness
    curFitness=0
    #keeping the number of lines of the current fitness
    cnt_linesCur=MAX_LINES
    #keeping the locations of the groups in the lines of the current solution
    linesCur=[]
    #performing ACO on a colony of ants for Niter times
    for i in range(Niter):
        #getting the best solution from the ants
        curFitness,cnt_linesCur,linesCur=allAnts(pheromones,groups)
        #updating the pheromones according to the best ant
        updatePheromones(pheromones,curFitness)
        if curFitness>bestFitness and cnt_linesCur<=cnt_lines:
            bestFitness=curFitness
            cnt_lines=cnt_linesCur
            lines=linesCur
    print(bestFitness)
    print(cnt_lines)
    print(lines)

    
    
    
    
    