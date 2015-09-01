#Variacion de los individuos
#Aplicar lo operadores
#los individuos padres provienen de un algoritmo
#especial, donde se seleccionan los mejores de cada especie
#las probabilidades de cruce y mutacion, son las mismas
#que se manejan en todos los algoritmos.
#n es el numero de hijos descendientes que se espera que regrese
#la clase, este parametro podria ser omitido
import random
from neat_gp import *
def neatGP(toolbox,parents,cxpb,mutpb,n):
    R=list()
    i=0
    while i<n:
        eflag=random.random()
        if eflag:
            ind1=parents[0] #el mejor individuo debido su fitnes
        else:
            ind1=random.choice(parents)
        if random.random()<mutpb:
            offspring=toolbox.mutate(ind1)
            del offspring[i].fitness.values
            del offspring[i].specie
            del offspring[i].fitness_sharing
            del offspring[i].num_specie
            offspring[i].descendents(offspring[i].get_descendents-1)
            i+=1
        if random.random()<cxpb:
            print'la mejor de la especie'
