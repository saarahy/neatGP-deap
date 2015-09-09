from deap import base, creator, gp, tools
from measure_tree import *
#Inicializa las poblacion con una sola especie
def init_species(population):
    for ind in population:
        ind.specie(1)

#cuenta el numero de especies en total
#de toda la poblacion
def count_species(population):
    specie=list()
    #specie.append(0)
    for ind in population:
        if ind.get_specie()!= None and ind.get_specie() not in specie:
            specie.append(ind.get_specie())
    if not specie:
        return 0
    else:
        return len(specie)

#funcion para contar los individuos de una especie
def ind_specie(population):
    specie=list()
    num=list()
    for ind in population:
        specie.append(ind.get_specie())
    specie.sort()
    for i in range(len(specie)):
        if specie[i]!=specie[i-1]:
            num.append([specie[i],specie.count(specie[i])])
    for ind in population:
        set_numind(ind, num)
    return num

#regresa el numero de individuos en una especie dada
def get_specie_ind(individuo, population):
    cont=0
    specie=individuo.get_specie()
    for ind in population:
        if ind.get_specie()==specie:
            cont+=1
    return cont

#funcion para asignar el numero de individuos
#en la especie, al individuo de esa misma especie

def set_numind(ind,species):
    for i in range(len(species)):
        if species[i][0]==ind.get_specie() and ind.num_specie!=None:
            ind.num_specie(species[i][1])

#revisa si algun individuo de la poblacion
#se encuentra sin especie y le asigna una
def species(population, h):
    for ind in population:
        if ind.get_specie()==None:
            for ind1 in population:
                if distance(ind,ind1)<=h:
                    ind.specie(ind1.get_specie())
                    break
            if ind.get_specie()==None:
                num_specie=count_species(population)
                ind.specie(num_specie+1)
    return population



