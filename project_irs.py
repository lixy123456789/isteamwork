import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib


# Define the container dimensions
container_length = 12050
container_width = 2320
container_height = 2550

volume_container = container_length * container_width * container_height;

# Constants for genetic algorithm
population_size = 2000
num_generations = 5

def check(flag_loc, flag_item, orientation, exist_item, locs, items_out, population, fitness, items):
    fitness_percentage = 0
    for two_orient in range(2):
        if two_orient==1:
            if orientation==0:
                orientation=1
            else:
                orientation=0
        prop_x1 = flag_loc[0]
        prop_y1 = flag_loc[1]
        prop_z1 = flag_loc[2]
        if orientation == 0:
            prop_x2 = prop_x1 + flag_item[1]
            prop_y2 = prop_y1 + flag_item[2]
            prop_z2 = prop_z1 + flag_item[3]
        else:
            prop_x2 = prop_x1 + flag_item[2]
            prop_y2 = prop_y1 + flag_item[1]
            prop_z2 = prop_z1 + flag_item[3]

        single_population = [flag_item[0], flag_item[1], flag_item[2], flag_item[3], flag_item[4], orientation, prop_x1, prop_y1, prop_z1, flag_item[5]]

        fit = False
        flow = False                
        if prop_x2 <= container_length \
            and prop_y2 < container_width \
            and prop_z2 < container_height:

            fit = True
            if prop_z1==0:
                flow = False
            else:
                flow = True

            for pop in population:
                x1 = pop[6]
                y1 = pop[7]
                z1 = pop[8]
                if pop[5]==0:
                    x2 = pop[6] + pop[1]
                    y2 = pop[7] + pop[2]
                    z2 = pop[8] + pop[3]
                else:
                    x2 = pop[6] + pop[2]
                    y2 = pop[7] + pop[1]
                    z2 = pop[8] + pop[3]


                if ((prop_y1 < y2 and \
                    prop_y2 > y1 and \
                    prop_z1 < z2 and \
                    prop_z2 > z1 and \
                    prop_x1 < x2 and \
                    prop_x2 > x1) or\
                    (prop_x1 == x1 and\
                    prop_y1 == y1 and\
                    prop_z1 == z1)):

                    fit = False
                    break

                if flow and prop_z1 > 0 and prop_x1 >= x1 and x2 >=prop_x1 and prop_y1 >= y1 and y2 >= prop_y1 and prop_z1 == z2:
                    flow = False
                  

        if fit and not(flow):
            population.append(single_population)

            volume = single_population[1] * single_population[2] * single_population[3]
            percentage = volume / volume_container * 100
            fitness_percentage = percentage

            array_to_append = [prop_x1, prop_y2, prop_z1]
            locs.append(array_to_append)
            array_to_append = [prop_x2, prop_y1, prop_z1]
            locs.append(array_to_append)
            array_to_append = [prop_x1, prop_y1, prop_z2]
            locs.append(array_to_append)

            items_out=True
            break
        else:
            if two_orient==1:
                exist_item.append(flag_item)

    return exist_item, locs, items_out, population, fitness_percentage


def initialize(items):
    best_fitness = 0
    fitness_array = []
    population_array = []
    for pop_size in range(population_size):
        locs = [(0,0,0)]
        exist_item = []
        exist_loc = []

        #population 0=id, 1=length, 2=width, 3=height, 4=weight, 5=orientation, 6=x1, 7=y1, 8=z1, 9=color
        population = []
        fitness = []

        locs_out = False
        while not(locs_out):
            flag_loc = []
            there_loc = False
            for loc in locs:
                flag_loc = loc
                there_loc1 = True
                for exist_loc1 in exist_loc:
                    if ((loc[0]==exist_loc1[0]) and (loc[1]==exist_loc1[1]) and (loc[2]==exist_loc1[2])):
                        there_loc1 = False
                        break
                if there_loc1:
                    there_loc = True
                    break

            if not(there_loc):
                locs_out = True
            else:
                exist_item = []
                random.shuffle(items)

                # random orientation 0=portrait 1=landscape
                orientation = random.randint(0, 1)
                items_out = False
                while not(items_out):
                    flag_item = []
                    there_item = False
                    for item in items:
                        flag_item = item
                        there_item1 = True
                        for pop in population:
                            if item[0]==pop[0]:
                                there_item1 = False
                                break

                        if there_item1:
                            for exist_item1 in exist_item:
                                if (item[0]==exist_item1[0]):
                                    there_item1 = False
                                    break

                        if there_item1:
                            there_item = True
                            break
                    
                    if not(there_item):
                        items_out = True
                        exist_loc.append(flag_loc)
                    else:
                        exist_item, locs, items_out, population, fitness_percentage = check(flag_loc, flag_item, orientation, exist_item, locs, items_out, population, fitness, items)


        population_array.append(population)

    fitness_array = []
    for pops in population_array:
        weight_flag = False
        for pop in pops:
            if pop[8]>0:
                check_x1 = pop[6]
                check_y1 = pop[7]
                check_z1 = pop[8]
                if pop[5]==0:
                    check_x2 = check_x1 + pop[1]
                    check_y2 = check_y1 + pop[2]
                    check_z2 = check_z1 + pop[3]
                else:
                    check_x2 = check_x1 + pop[2]
                    check_y2 = check_y1 + pop[1]
                    check_z2 = check_z1 + pop[3]
                check_weight = pop[4]

                for other_pop in pops:
                    if not(pop[0]==other_pop[0]):
                        x1 = other_pop[6]
                        y1 = other_pop[7]
                        z1 = other_pop[8]
                        if other_pop[5]==0:
                            x2 = x1 + other_pop[1]
                            y2 = y1 + other_pop[2]
                            z2 = z1 + other_pop[3]
                        else:
                            x2 = x1 + other_pop[2]
                            y2 = y1 + other_pop[1]
                            z2 = z1 + other_pop[3]
                        w = other_pop[4]

                        if (((x1 <= check_x1 <= x2) and (y1 <= check_y1 <= y2) and (check_z1 >= z2) and check_weight > w) or \
                            ((x1 <= check_x2 <= x2) and (y1 <= check_y1 <= y2) and (check_z1 >= z2) and check_weight > w) or \
                            ((x1 <= check_x1 <= x2) and (y1 <= check_y2 <= y2) and (check_z1 >= z2) and check_weight > w) or \
                            ((x1 <= check_x2 <= x2) and (y1 <= check_y2 <= y2) and (check_z1 >= z2) and check_weight > w)):
                            weight_flag = True
                            break
                
            if weight_flag:
                break

        if weight_flag:
            #print("WEIGHT FLAG: ", weight_flag)
            fitness_percentage = -100000
        else:
            volume = 0
            for pop in pops:
                volume = volume + (pop[1] * pop[2] * pop[3])
            percentage = volume / volume_container * 100
            fitness_percentage = percentage

        fitness_array.append(fitness_percentage)

    return population_array, fitness_array



def crossover(pop1, pop2, crossover_rate, items):
    new_population = []

    locs = [(0,0,0)]
    for count_pop in range(crossover_rate):
        new_population.append(pop1[count_pop])

        #population 0=id, 1=length, 2=width, 3=height, 4=weight, 5=orientation, 6=x1, 7=y1, 8=z1, 9=color
        prop_x1 = pop1[count_pop][6]
        prop_y1 = pop1[count_pop][7]
        prop_z1 = pop1[count_pop][8]
        if pop1[count_pop][5] == 0:
            prop_x2 = prop_x1 + pop1[count_pop][1]
            prop_y2 = prop_y1 + pop1[count_pop][2]
            prop_z2 = prop_z1 + pop1[count_pop][3]
        else:
            prop_x2 = prop_x1 + pop1[count_pop][2]
            prop_y2 = prop_y1 + pop1[count_pop][1]
            prop_z2 = prop_z1 + pop1[count_pop][3]

        array_to_append = [prop_x1, prop_y2, prop_z1]
        locs.append(array_to_append)
        array_to_append = [prop_x2, prop_y1, prop_z1]
        locs.append(array_to_append)
        array_to_append = [prop_x1, prop_y1, prop_z2]
        locs.append(array_to_append)
    
    count_pop = -1
    for i in range(crossover_rate, len(pop2)):
        count_pop = count_pop + 1
        check_exist = False
        for j in range(len(new_population)):
            if new_population[j][0] == pop2[count_pop][0]:
                check_exist = True
                break
        
        flag_loc = []
        if not(check_exist):
            flag_loc = [pop2[count_pop][6], pop2[count_pop][7], pop2[count_pop][8]]

            for item in items:
                if item[0]==pop2[count_pop][0]:
                    flag_item = item
                    break
            
            orientation = pop2[count_pop][5]

            exist_item = []
            items_out = False
            exist_item, locs, items_out, new_population, fit = check(flag_loc, flag_item, orientation, exist_item, locs, items_out, new_population, [], items)

    exist_item = []
    for new_pop in new_population:
        for item in items:
            if item[0]==new_pop[0]:
                item_to_array = item
                exist_item.append(item_to_array)

    ####
    locs_out = False
    exist_loc = []
    while not(locs_out):
        flag_loc = []
        there_loc = False
        for loc in locs:
            flag_loc = loc
            there_loc1 = True
            for exist_loc1 in exist_loc:
                if ((loc[0]==exist_loc1[0]) and (loc[1]==exist_loc1[1]) and (loc[2]==exist_loc1[2])):
                    there_loc1 = False
                    break
            if there_loc1:
                there_loc = True
                break

        if not(there_loc):
            locs_out = True
        else:
            exist_item = []
            random.shuffle(items)

            # random orientation 0=portrait 1=landscape
            orientation = random.randint(0, 1)
            items_out = False
            while not(items_out):
                flag_item = []
                there_item = False
                for item in items:
                    flag_item = item
                    there_item1 = True
                    for pop in new_population:
                        if item[0]==pop[0]:
                            there_item1 = False
                            break

                    if there_item1:
                        for exist_item1 in exist_item:
                            if (item[0]==exist_item1[0]):
                                there_item1 = False
                                break

                    if there_item1:
                        there_item = True
                        break
                
                if not(there_item):
                    items_out = True
                    exist_loc.append(flag_loc)
                else:
                    exist_item, locs, items_out, new_population, fit = check(flag_loc, flag_item, orientation, exist_item, locs, items_out, new_population, [], items)


    return new_population




def do_crossover(population, fitness, items):
    sorted_fitness = sorted(fitness, reverse=True)

    half_pop = int(population_size/2)
    kk=-1
    for k in range(half_pop):
        kk=kk+1
        ll=kk
        kk=kk+1
        mm=kk
        pop1 = population[fitness.index(sorted_fitness[ll])]
        pop2 = population[fitness.index(sorted_fitness[mm])]

        if len(pop1) < len(pop2):
            min_len = len(pop1)
        else:
            min_len = len(pop2)
        crossover_rate = random.randint(0, min_len)

        new_population = crossover(pop1, pop2, crossover_rate, items)
        population.append(new_population)


        pop1 = population[fitness.index(sorted_fitness[mm])]
        pop2 = population[fitness.index(sorted_fitness[ll])]
        new_population = crossover(pop1, pop2, crossover_rate, items)
        population.append(new_population)
        #new_temp_population = population[:start_pop:end_pop]

        start_pop = len(fitness)
        end_pop = len(population)

        new_temp_population = []
        for i in range(start_pop, end_pop):
            new_temp_population.append(population[i])

        fitness_array = fitness
        for pops in new_temp_population:
            weight_flag = False
            for pop in pops:
                if pop[8]>0:
                    check_x1 = pop[6]
                    check_y1 = pop[7]
                    check_z1 = pop[8]
                    if pop[5]==0:
                        check_x2 = check_x1 + pop[1]
                        check_y2 = check_y1 + pop[2]
                        check_z2 = check_z1 + pop[3]
                    else:
                        check_x2 = check_x1 + pop[2]
                        check_y2 = check_y1 + pop[1]
                        check_z2 = check_z1 + pop[3]
                    check_weight = pop[4]

                    for other_pop in pops:
                        if not(pop[0]==other_pop[0]):
                            x1 = other_pop[6]
                            y1 = other_pop[7]
                            z1 = other_pop[8]
                            if other_pop[5]==0:
                                x2 = x1 + other_pop[1]
                                y2 = y1 + other_pop[2]
                                z2 = z1 + other_pop[3]
                            else:
                                x2 = x1 + other_pop[2]
                                y2 = y1 + other_pop[1]
                                z2 = z1 + other_pop[3]
                            w = other_pop[4]

                            if (((x1 <= check_x1 <= x2) and (y1 <= check_y1 <= y2) and (check_z1 >= z2) and check_weight > w) or \
                                ((x1 <= check_x2 <= x2) and (y1 <= check_y1 <= y2) and (check_z1 >= z2) and check_weight > w) or \
                                ((x1 <= check_x1 <= x2) and (y1 <= check_y2 <= y2) and (check_z1 >= z2) and check_weight > w) or \
                                ((x1 <= check_x2 <= x2) and (y1 <= check_y2 <= y2) and (check_z1 >= z2) and check_weight > w)):
                                weight_flag = True
                                break
                    
                if weight_flag:
                    break

            if weight_flag:
                fitness_percentage = -100000
            else:
                volume = 0
                for pop in pops:
                    volume = volume + (pop[1] * pop[2] * pop[3])
                percentage = volume / volume_container * 100
                fitness_percentage = percentage

            fitness_array.append(fitness_percentage)

    return population, fitness_array


def genetic_algorithm(population_size, num_generations, items):
    population, fitness = initialize(items)

    for i in range(num_generations):
        population, fitness = do_crossover(population, fitness, items)

        sorted_fitness = sorted(fitness, reverse=True)
        best_fitness = sorted_fitness[0]
        best_population = population[fitness.index(sorted_fitness[0])]
        print("BEST FITNESS IN GENERATION ", i, " : ", round(best_fitness,2), " with Number of Items in Container : ", len(best_population))


    sorted_fitness = sorted(fitness, reverse=True)
    best_fitness = sorted_fitness[0]
    best_population = population[fitness.index(sorted_fitness[0])]


    return best_population, best_fitness


def get_population(items):
    population = []
    fitness = []
    best_fitness = 0
    population, best_fitness = genetic_algorithm(population_size, num_generations, items)
    print(len(population), population)
    return population

