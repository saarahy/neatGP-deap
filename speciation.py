from deap import base, creator, gp, tools
from measure_tree import *
def init_species(population):
    for ind in population:
        ind.specie(1)

def count_species(population):
    contador=0
    for ind in population:
        if ind.get_specie!= None:
            contador+=1
    return contador

def species(population, h):
    for ind in population:
        if ind.get_specie==None:
            for ind1 in population:
                if distance(ind,ind1)<=h:
                    ind.specie=ind1.get_specie()
                    break
            if ind.get_specie==None:
                num_specie=count_species(population)
                ind.specie=num_specie+1
    return population


