from asyncio.windows_events import NULL
from operator import index
import random
import bird
import settings as val

def advanced(group):
    check_fitness(group)
    bird_array = advanced_selection(val.NEW_POPULATION, group)
    return bird_array
    
def create_population(group):
    new_birds=[]
    check_fitness(group)
    for i in range(val.NEW_POPULATION):
        new1 =pool_selection(group)
        if new1!=NULL:
            new_birds.append(new1)
            #new_birds.append(new2)

    return new_birds

index=-1
def pool_selection(group):
    '''
    #seletion for the fittest bird
    global index
    if index >= -100:
        parent1=group[index]

    index2=index + -1
    if index >=-100:
        parent2=group[index2]

    index+=-1 

    '''

    
      
    
    index1 = 0
    rand1 = random.randint(0, 1)
    while(rand1 > 0 ):
        if(index1>val.NEW_POPULATION-1):
            index1=random.randint(0, val.NEW_POPULATION)
            break
        else:
            rand1 = rand1 - group[index1].fitness
        #print(rand1, group[index1].fitness)
            index1+=1
    index1-=1


    parent1 = group[index1]

    index2 = 1
    rand2 = random.randint(0, 1)
    while(rand2 > 0):
        if(index2 > val.NEW_POPULATION-1):
            index2=random.randint(0, val.NEW_POPULATION)
            break
        else:
            rand2 = rand2 - group[index2].fitness
            index2+=1
    index2-=1
    '''

    #parent2 = group[index2]

    #if (abs(parent1.fitness-parent2.fitness)<= max(parent1.fitness, parent2.fitness)/2):

    #print("fitness", parent1.fitness ,parent2.fitness, parent1.brain.o_biases, parent1.brain.h_weights)
    offspring = bird.Bird(200, 200, bird.screen, parent1.brain)
    offspring2 = bird.Bird(200, 200, bird.screen, parent2.brain)
    #print(offspring.brain.o_biases, offspring.brain.h_weights)
    '''
    parent2=group[index2]
    offspring = bird.Bird(200, 200, bird.screen, False )#parent1.brain)
    #offspring2=  bird.Bird(200, 200, bird.screen, False )
        #crossover
    
    hidden_input_weights = parent1.brain.h_weights
    hidden_output_weights = parent1.brain.o_weights
    hidden_input_weights2 = parent2.brain.h_weights
    hidden_output_weights2 = parent2.brain.o_weights

    bias_in = parent1.brain.h_biases
    bias_out = parent1.brain.o_biases
    bias_in2 = parent2.brain.h_biases
    bias_out2 = parent2.brain.o_biases

    offspring.brain.crossover( hidden_input_weights , hidden_output_weights, 
    hidden_input_weights2, hidden_output_weights2, bias_in, bias_out, bias_in2, bias_out2)

    #offspring.brain.crossover(hidden_input_weights2, hidden_output_weights2, hidden_input_weights, hidden_output_weights,
    #bias_in2, bias_out2, bias_in, bias_out)

    #offspring2.brain.mutate(0.3)
    offspring.brain.mutate(0.3)

    return offspring #offspring2

    pass
    
    return offspring, offspring2

def check_fitness(group):
    
    total_score=1
    cls_dist = 1

    for bird in group:
        total_score+=bird.score

    for bird in group:
        #bird.fitness = bird.score/total_score     
        bird.fitness = (bird.score + bird.cls_dist)/ (total_score + cls_dist)
        #print(bird.fitness, bird.score, bird.cls_dist)
        #print(bird.fitness)
'''
        if bird.score >2:
            print("weights", bird.brain.h_weights)
            print("bias", bird.brain.h_biases)
            print("o_weights", bird.brain.o_weights)
            print("o_bias", bird.brain.o_biases)
'''        

def advanced_selection(n, group):
    next_pop=[]
    first_ratio_num = 0.4 * n
    ratio_num = int(len(group)-first_ratio_num)
    best_bird = group[ratio_num:]
    for i in best_bird:
        next_pop.append(i)

    
    second_ratio_num = 0.2 * n
    for i in range(round(second_ratio_num/2)):
        index = -2
        parent1 = group[-1]
        parent2= group[index]

        offspring = bird.Bird(200, 200, bird.screen, False)#parent1.brain)
        offspring2 =bird.Bird(200, 200, bird.screen, False)#parent1.brain)
    #offspring2=  bird.Bird(200, 200, bird.screen, False )
        #crossover
    
        hidden_input_weights = parent1.brain.h_weights
        hidden_output_weights = parent1.brain.o_weights
        hidden_input_weights2 = parent2.brain.h_weights
        hidden_output_weights2 = parent2.brain.o_weights

        bias_in = parent1.brain.h_biases
        bias_out = parent1.brain.o_biases
        bias_in2 = parent2.brain.h_biases
        bias_out2 = parent2.brain.o_biases

        offspring.brain.crossover( hidden_input_weights , hidden_output_weights, 
        hidden_input_weights2, hidden_output_weights2, bias_in, bias_out, bias_in2, bias_out2)
        offspring2.brain.crossover(hidden_input_weights2, hidden_output_weights2, 
        hidden_input_weights, hidden_output_weights, bias_in2, bias_out2, bias_in, bias_out)
        
        offspring.brain.mutate(0.3)
        offspring2.brain.mutate(0.3)

        next_pop.append(offspring)
        next_pop.append(offspring2)
        index += -1

    for i in range(round(second_ratio_num/2)):
        index = -3
        parent1 = group[-2]
        parent2 = group[index]

        offspring = bird.Bird(200, 200, bird.screen, False )
        offspring2 =bird.Bird(200, 200, bird.screen, False) #parent1.brain)
    #offspring2=  bird.Bird(200, 200, bird.screen, False )
        #crossover
    
        hidden_input_weights = parent1.brain.h_weights
        hidden_output_weights = parent1.brain.o_weights
        hidden_input_weights2 = parent2.brain.h_weights
        hidden_output_weights2 = parent2.brain.o_weights

        bias_in = parent1.brain.h_biases
        bias_out = parent1.brain.o_biases
        bias_in2 = parent2.brain.h_biases
        bias_out2 = parent2.brain.o_biases

        offspring.brain.crossover( hidden_input_weights , hidden_output_weights, 
        hidden_input_weights2, hidden_output_weights2, bias_in, bias_out, bias_in2, bias_out2)
        offspring2.brain.crossover(hidden_input_weights2, hidden_output_weights2, 
        hidden_input_weights, hidden_output_weights, bias_in2, bias_out2, bias_in, bias_out)

        offspring.brain.mutate(0.3)
        offspring2.brain.mutate(0.3)
        
        next_pop.append(offspring)
        next_pop.append(offspring2)

        index += -1

    third_ratio = 0.2 * n
    for i in range(int(third_ratio)):
        rand = random.randint(-3, -1)
        parent = group[rand]
        offspring = bird.Bird(200, 200, bird.screen, parent.brain)
        offspring.brain.mutate(0.3)
        next_pop.append(offspring)


    return next_pop
