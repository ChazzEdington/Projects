#Needs maze_samples.py to run and maze.py to visualize. Remaining files can be
#found on https://github.com/ChazzEdington/hello-world in support folder

import maze
import maze_samples
import random

#-----------------------------Define-Individual-------------------------------


class Individual:

  def __init__(self, length, genotype):

    self.length = length
    self.genotype = genotype
    
    if self.genotype == '':
      self.create()

    self.fitness = 0
    
    self.det_fitness()

  def create(self):

    move = 'UDLR'

    #Creates random invidiual
    for letter in range(self.length):
      self.genotype += move[random.randint(0, 3)]


    #---------------------Fitness------------------------


  def det_fitness(self):

    #keep track of maze position
    maze_ = maze_samples.maze[maze_case]

    #Keep track if mouse is within bounds of the game
    width = len(maze_[0])
    height = len(maze_)

    #row_start and col_start are global variables determined in
    #main function. Global for ease of use
    row = row_start
    col = col_start

    #Values to determine fitness
    repeat = None
    cheese = 0
    path = 0
    wall = 0
    off_board = 0
    bonus = 0     #number in a row on a path

    previous_opposite = ''

    #Keeps track of location of the mouse, tally what type of block
    #The mouse has landed on
    for move in self.genotype:

      if move == 'U':
        row += 1
        repeat_hold = 'D'

      elif move == 'D':
        row -= 1
        repeat_hold = 'U'

      elif move == 'L':
        col -=1
        repeat_hold ='R'

      elif move == 'R':
        col += 1
        repeat_hold = 'L'

      else:
        print('Improper move')

      #Check if off board, if is take note and move on
      if row >= height or row < 0 or col >= width or col < 0:
        off_board += 1
        continue
      
      
      elif maze_[row][col] == 'C':
        cheese += 1

        #If cheese is found and if mouse stayed on path, game is won
        if cheese == 1 and wall == 0 and off_board == 0:
          self.fitness = 'Won'
          return 'Won'

      elif maze_[row][col] == '-':
        path += 1
      
        if wall == 0 and off_board == 0:
          bonus += 1

        #penalize mouse for backtracking, avoids circular tracks to be
        #overly 'fit'
        if maze_[row][col] == repeat:
          path -= .5

          if bonus > 0:
            bonus -=.5
          

      elif maze_[row][col] == 'x' or maze_[row][col] == 'M':
        wall += 1

      repeat = repeat_hold
       

    #fitness function. Start with positive amount so that functions don't go
    #below 0. Add points for moves along path, points for
    #making it to cheese at an exponential rate if path was taken part of way.
    #Subtract points for hitting the wall and going off board.
    self.fitness = int(3*self.length) + 10*path + (10*cheese)**(bonus+path +2)\
                   + path**bonus- wall - 3*off_board


  #Allows fitness to be retrieved by int() call on class
  def __int__(self):
    return self.fitness



  #allows genotype to be retrieved by str() call on class
  def __str__(self):
    
    return self.genotype

#------------------------------Store-Population--------------------------------

class Population:

  def __init__(self, name):

    self.generation = name
    self.population = []

  #gives the generation that the population belongs to
  def __str__(self):
    return str(self.generation)

  #adds to the population
  def add(self, individual):

    self.population.append(individual)

  #empties past generations in an attempt to keep memory free
  def clear(self):
    self.population = ''

#--------------------------Genetic-Algorithm---------------------------------
    

class GA:

  def __init__(self, population_size, string_length, trials):


    #Initialization values
    self.size = population_size
    self.length = string_length
    self.trials = trials

    #Hold the determined fittest so can be retrieved after GA ran if wanted
    self.fittest = ''

    #population/generation set up
    self.generation = [Population(i) for i in range(trials)]
    self.current = self.generation[0]         #always keeps current generation

    #First generation creation
    for i in range(self.size):
      self.current.add(Individual(self.length, ''))

    #For monte carlo
    self.selection_weights= []
    


      #---------------------Monte-Carlo------------------------

  #Same as given
    
  def Set_Weights_Monte_Carlo(self, keys):

    normalized_values = [int(v/sum(keys)*100+.5) for v in keys]
    accum = 0

    for w in normalized_values:
      accum += w
      self.selection_weights.append(accum)


  def Monte_Carlo_Selection(self):

    select = random.randint(0, self.selection_weights[-1])
    for position, weight in enumerate(self.selection_weights):
      if select <= weight:

        return position
    

      #---------------------Perform-Trials(Generations)------------

  def run(self):

    for gen in range(1, self.trials):


      highest_fit = 0
      runner_up = 0
      
      keys = []
      
      for individual in self.current.population:

        #Try except statement to test if game has been won. Known since
        #Genotype that wins has fitness of 'won'
        try:
          x = int(individual)             
          keys.append(x)

          #Hold the most and 2nd most fit individuals for elitism
          if x > highest_fit:
            most_fit = str(individual)
            highest_fit = x

          elif x > runner_up:
            second_fit = str(individual)
            runner_up = x

        #break from algorithm if a solution is found which is known when
        #A string not not int is found in the fitness
        except TypeError:
          print(str(individual), ' genotype in generation ', gen, ' completed maze')
          self.fittest = str(individual)
          return(str(individual))

      #Clear selection weights each call
      self.selection_weights= []

      #Set monte carlo weights
      self.Set_Weights_Monte_Carlo(keys)

      #Crossbreed and make new individuals
      self.crossbreed(gen, most_fit, second_fit)

      #Set new current generation, erase previous
      self.current = self.generation[gen]
      self.generation[gen-1].clear()

    #if winning solution never found, return fittest of final generation
    self.fittest = most_fit
    print('Most fit individual of the population: ',self.fittest)
    return self.fittest


      #---------------------Crossbreed------------------------


  def crossbreed(self, gen, most_fit, second_fit):

    #Run until entire new generation is complete 
    for i in range(int(.5*len(self.current.population))-1):
      
      p1 = str(self.current.population[self.Monte_Carlo_Selection()])
      p2 = str(self.current.population[self.Monte_Carlo_Selection()])
      split = random.randint(0, self.length -1)

    #Combine parents at randomly determined at split location
    #send 'baby' to be potentially mutated
      baby1 = p1[:split] + p2[split:]
      baby1 = self.mutate(baby1)

      baby2 = p2[:split] + p1[split:]
      baby2 = self.mutate(baby2)
  
      self.generation[gen].add(Individual(self.length, baby1))
      self.generation[gen].add(Individual(self.length, baby2))

    #Call to add the top two individuals to the new generation
    self.elitism(gen, most_fit, second_fit)


    #----------------------elisism-----------------------

  def elitism(self, gen, most_fit, second_fit):
    #used to maintain top individuals from a population
    #Hopefully increase odds of moving to a correct sokutuon

    self.generation[gen].add(Individual(self.length, most_fit))
    self.generation[gen].add(Individual(self.length, second_fit))
    
      


      #---------------------Mutate------------------------

  def mutate(self, baby):

    move = 'UDLR'

    r = random.randint(1, 100)
    rate = 30

    if r < rate:

      position = random.randint(0, self.length-1)
      new_gene = move[random.randint(0, len(move)-1)]
      new_geno = baby[:position] + new_gene + baby[position+1:]

      #If mutated return the new genotype
      return new_geno

    #If not, return itself
    return baby

    

  
#--------------------------Main-Function--------------------------------------  

def main():
  # There are currently 2 samples in maze_samples.py
  global maze_case
  maze_case = 0

  maze_ = maze_samples.maze[maze_case]

  #determine start location
  for row in range(len(maze_)):
    
    for col in range(len(maze_[row])):
      if maze_[row][col] == 'M':

        global col_start
        col_start = col

        global row_start
        row_start = row

        break;


  string_length = maze_samples.string_length[maze_case]
  #Can change trials and population as needed
  population_size = 1000
  trials = 1000

  #Initializes genetic algoroith
  x = GA(population_size, string_length, trials)

  #runs maze and returns the fittest individual, or any that completed it
  fittest = x.run()


  #Visualize the maze
  M = maze.Maze(maze_samples.maze[maze_case]) 
  M.Visualize()
  M.RunMaze(fittest) 

if __name__=='__main__' :
  main()



