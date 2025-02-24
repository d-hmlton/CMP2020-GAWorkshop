# vacuum.py
#
# The code that defines the behaviour of the vacuum. 
#
# Written by: Simon Parsons
# Modified by: Helen Harman
# Last Modified: 01/02/24

import world
import random
import config
import utils

from numpy.random import randint # https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html
from numpy.random import rand    # https://numpy.org/doc/stable/reference/random/generated/numpy.random.rand.html

class GA():
    def __init__(self, world):
        # Make a copy of the world an attribute, so that Link can
        # query the state of the world
        self.world = world
        
        # initialise the population with randomly generated individuals
        self.population = [randint(0, config.numberOfLocations, config.numberOfQueens).tolist() for _ in range(config.populationSize)]
        
        
        # calculate the fitness of the initial population
        self.fitnesses = []
        self.best_fitness = -1
        self.best_individual = None
        self.calculateFitnessOfPopulation()
        
    # Create a new population and 
    # return the best individual found so far.
    def makeMove(self):
        # create the next generation
        children = []
        for i in range(0, len(self.population), 2):
            # get selected parents in pairs
            parent1 = self.performTournamentSelection() 
            parent2 = self.performTournamentSelection() 
            
            child1, child2 = self.performCrossover(parent1, parent2)
                
            child1 = self.performMutation(child1)    
            child2 = self.performMutation(child2)       
            	
            children.append(child1)
            children.append(child2)
            
        # replace population
        self.population = children
        self.calculateFitnessOfPopulation()
        return (self.best_individual, self.best_fitness)   
        
        
        
    #####################################  
    # Modify these methods: 
       
    def performTournamentSelection(self, k=3):
        # you need to write this method
        # Select k random individuals from self.population. 
        # Select the best individual from the k individuals (individual with the lowest fitness) and return it.
        #  The fitnesses of the population are stored in self.fitnesses.   
        #   i.e. the fitness of self.population[i] is self.fitnesses[i]

        #Since population and fitness become uncoupled when randomising the population, resolving that by pairing them up in another list
        individualFitnessPairs = []
        for pair in range(len(self.population)):
            individualFitnessPairs.append([self.population[pair], self.fitnesses[pair]])

        #Creates a random sample of 'k' (by default, 3) individuals from the population
        sampleList = random.sample(individualFitnessPairs, k)

        #Saves the fitness of the first individual to int 'lowest'. Will be compared to others
        lowest = sampleList[0][1]

        for individual in range(1, len(sampleList)): #Starts at pos 1 - skips pos 0 since it's already 'lowest'
            if sampleList[individual][1] <= lowest: #"less than or equal to" - biased towards new solutions of equal value
                lowest = individual

        print(sampleList[lowest][1])
        return sampleList[lowest][0] #Returns the individual with the lowest fitness (or, if equally low, the furthest along the sample)
    
    
    def performCrossover(self, parent1, parent2): 
        # you need to write this method

        crossoverRandom = random.randint(0, 10) #Generate value somewhere in crossover rate range (need to divide by 10 after)

        if (crossoverRandom / 10) < config.crossoverRate: #If the random value is below the crossover rate:
            crossoverRandom = random.randint(1, 6)
            child1 = parent1.copy() #Saves parent 1's list to 'child1'
            child2 = parent2.copy() #Saves parent 2's list to 'child2'
            for x in range(crossoverRandom, 7): #From the crossover point to the end of the child, swaps values to be other parent
                child1[x] = parent2[x]
                child2[x] = parent1[x]
            return [child1, child2] #Returns children

        else: #If the random value is above or equal to the crossover rate:
            return [parent1.copy(), parent2.copy()] #Returns (copy of) parents
       
        
    def performMutation(self, individual): 
        # you need to write this method
        
        #Mutator
        for gene in range(len(individual)): #Cycles through all the 'genes'
            mutationRandom = random.randint(0, 10) #Generate value in mutation rate range (0.1 by default)
            print(mutationRandom / 10, config.mutationRate)
            if (mutationRandom / 10) < config.mutationRate: #If below the mutation rate:
                while True:
                    mutationRandom = random.randint(0, (config.numberOfLocations - 1)) #Generate an integer for the mutation
                    if individual[gene] != mutationRandom:
                        break
                individual[gene] = mutationRandom #Save the integer over the original gene
        
        return individual
       
    #  End of methods you need to modify
    #####################################   
    
    ##
    # Methods for fitness calculations    
        
    def calculateFitnessOfPopulation(self):
        self.fitnesses = [self.calculateFitness(i) for i in self.population]

        # check for new best solution		
        for i in range(len(self.population)):
            if ((self.best_individual == None) or (self.fitnesses[i] < self.best_fitness)):
                self.best_fitness = self.fitnesses[i]
                self.best_individual = self.population[i]
        
    # count the number of collisions
    def calculateFitness(self, individual):
        total = 0
        for i in range(len(individual)): # Count the number of agents the ith agent collides with
            agent = utils.Pose(i, individual[i])
            for j in range(i+1, len(individual)):
                agent2 = utils.Pose(j, individual[j])
                if self.isColunmCollision(agent, agent2) or self.isRowCollision(agent, agent2) or self.isDiagonalCollision(agent, agent2):
                    total = total + 1
        return total           
            
    

    def isColunmCollision(self, pose1, pose2):
        return (pose1.y == pose2.y)
    def isRowCollision(self, pose1, pose2):
        return (pose1.x == pose2.x)
    def isDiagonalCollision(self, pose1, pose2):         
        return (abs(pose1.x - pose2.x) == abs(pose1.y - pose2.y))
        
        

    


