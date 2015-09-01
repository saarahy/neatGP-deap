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
from crosspoints import *
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
            #del offspring.fitness.values
            del offspring.specie
            del offspring.fitness_sharing
            del offspring.num_specie
            R.append(offspring)
            ind1.descendents(offspring[i].get_descendents()-1)
            i+=1
        if random.random()<cxpb:
            if ind1.get_numspecie()>1:
                for q in parents:
                    if q!=ind1 and q.get_fsharing()>=ind1.get_fsharing():
                        ind2=q
                        break
            else:
                ind2=random.choice(parents)
            hijo=neatcx(ind1,ind2)
            R.append(hijo)
            ind1.descendents(ind1.get_descendents()-0.5)
            ind2.descendents(ind2.get_descendents()-0.5)
            i+=1
            if ind2.get_descendents()<=0:
                print 'ayuda'
                #del parents[ind2]
        if ind1.get_descendents()<=0:
            print 'ayuda'
            #del parents[ind1]
    return R

