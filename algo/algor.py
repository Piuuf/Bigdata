import random
import os
import json
import time

class algoGenetique(object):

    def __init__(self,genes,individuals_length,decode,fitness):
        self.genes= genes
        self.individuals_length= individuals_length
        self.decode= decode
        self.fitness= fitness

    def mutation(self, chromosome, prob):

            def inversion_mutation(chromosome_aux):
                chromosome = chromosome_aux

                index1 = randrange(0,len(chromosome))
                index2 = randrange(index1,len(chromosome))

                chromosome_mid = chromosome[index1:index2]
                chromosome_mid.reverse()

                chromosome_result = chromosome[0:index1] + chromosome_mid + chromosome[index2:]

                return chromosome_result

            aux = []
            for _ in range(len(chromosome)):
                if random.random() < prob :
                    aux = inversion_mutation(chromosome)
            return aux

    def crossover(self,parent1, parent2):

        def process_gen_repeated(copy_child1,copy_child2):
            count1=0
            for gen1 in copy_child1[:pos]:
                repeat = 0
                repeat = copy_child1.count(gen1)
                if repeat > 1:#If need to fix repeated gen
                    count2=0
                    for gen2 in parent1[pos:]:#Choose next available gen
                        if gen2 not in copy_child1:
                            child1[count1] = parent1[pos:][count2]
                        count2+=1
                count1+=1

            count1=0
            for gen1 in copy_child2[:pos]:
                repeat = 0
                repeat = copy_child2.count(gen1)
                if repeat > 1:#If need to fix repeated gen
                    count2=0
                    for gen2 in parent2[pos:]:#Choose next available gen
                        if gen2 not in copy_child2:
                            child2[count1] = parent2[pos:][count2]
                        count2+=1
                count1+=1

            return [child1,child2]

        pos=random.randrange(1,self.individuals_length-1)
        child1 = parent1[:pos] + parent2[pos:]
        child2 = parent2[:pos] + parent1[pos:]

        return  process_gen_repeated(child1, child2)


def decodeVRP(chromosome):
    list=[]
    for (k,v) in chromosome:
        if k in trucks[:(num_trucks-1)]:
            list.append(frontier)
            continue
        list.append(cities.get(k))
    return list


def penalty_capacity(chromosome):
        actual = chromosome
        value_penalty = 0
        capacity_list = []
        index_cap = 0
        overloads = 0

        for i in range(0,len(trucks)):
            init = 0
            capacity_list.append(init)

        for (k,v) in actual:
            if k not in trucks:
                capacity_list[int(index_cap)]+=v
            else:
                index_cap+= 1

            if  capacity_list[index_cap] > capacity_trucks:
                overloads+=1
                value_penalty+= 100 * overloads
        return value_penalty

def fitnessVRP(chromosome):

    def distanceTrip(index,city):
        w = distances.get(index)
        return  w[city]

    actualChromosome = chromosome
    fitness_value = 0

    penalty_cap = penalty_capacity(actualChromosome)
    for (key,value) in actualChromosome:
        if key not in trucks:
            nextCity_tuple = actualChromosome[key]
            if list(nextCity_tuple)[0] not in trucks:
                nextCity= list(nextCity_tuple)[0]
                fitness_value+= distanceTrip(key,nextCity) + (50 * penalty_cap)
    return fitness_value
