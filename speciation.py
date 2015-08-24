from deap import base, creator, gp, tools
from measure_tree import *
def init_species(population):
    for ind in population:
        ind.specie(1)

def count_species():
    return 0

def species(population, h):
    for ind in population:
        if ind.specie==None:
            for ind1 in population:
                if distance(ind,ind1)<=h:
                    ind.specie=ind1.get_specie()
                    break
            if ind.specie==None:
                num_specie=count_species()
                ind.specie=num_specie+1


