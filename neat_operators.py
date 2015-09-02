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
def neatGP(toolbox,parents,population,cxpb,mutpb,n):
    r=list()
    i=0
    while i<n:
        eflag=int(round(random.random()))
        if len(parents)>0:
            if eflag:
                ind1=parents[0] #el mejor individuo debido su fitnes
            else:
                ind1=random.choice(parents)
        else:
                ind1=random.choice(population)
        if random.random()<mutpb:
            of=copy.deepcopy(ind1)
            offspring=toolbox.mutate(of)
            r.append(offspring[0])
            ind1.descendents(ind1.get_descendents()-1)
            i+=1
        if random.random()<cxpb:
            if ind1.get_numspecie()>1:
                for q in parents:
                    if q.get_specie()==ind1.get_specie():
                        ind2=q
                        break
            else:
                ind2=random.choice(parents)
            of1=copy.deepcopy(ind1)
            of2=copy.deepcopy(ind2)
            hijo=neatcx(of1,of2)
            r.append(hijo)
            ind1.descendents(ind1.get_descendents()-0.5)
            ind2.descendents(ind2.get_descendents()-0.5)
            i+=1
            if ind2.get_descendents()<=0:
                for i in range(len(parents)):
                    if parents[i] == ind2:
                        del parents[i]
                        break
        if ind1.get_descendents()<=0:
            for i in range(len(parents)):
                if parents[i] == ind1:
                    del parents[i]
                    break
    return r

