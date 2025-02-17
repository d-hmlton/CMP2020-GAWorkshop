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
        
        return [] # <-- remove this line when you have added your implementation
    
    
    
    def performCrossover(self, parent1, parent2): 
        # you need to write this method
        return [parent1.copy(), parent2.copy()] # <-- remove this line when you have added your implementation
       
       
        
    def performMutation(self, individual): 
        # you need to write this method
        return individual # <-- remove this line when you have added your implementation
       
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
        
        

    


