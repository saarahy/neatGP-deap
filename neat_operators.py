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
    r=list()
    i=0
    copy_parent=copy.deepcopy(parents)

    while i<n:
        bandera=0
        if n>len(copy_parent):
            lim=int(round(n/len(copy_parent)))
            lim=lim*2
            for d in range(lim):
                copy_parent+=copy_parent
        eflag=int(round(random.random()))
        if eflag:
            ind1=copy_parent[0] #el mejor individuo debido su fitnes
        else:
            ind1=random.choice(copy_parent)
        if random.random()<mutpb:
            bandera=1
            of=copy.deepcopy(ind1)
            offspring=toolbox.mutate(of)
            offspring[0].descendents(0)
            offspring[0].fitness_sharing(0)
            del offspring[0].fitness.values
            r.append(offspring[0])
            ind1.descendents(ind1.get_descendents()-1)
            i+=1
        if random.random()<cxpb:
            if ind1.get_numspecie()>1:
                for q in copy_parent:
                    if q.get_specie()==ind1.get_specie():
                        ind2=q
                        break
            else:
                ind2=random.choice(copy_parent)
            of1=copy.deepcopy(ind1)
            of2=copy.deepcopy(ind2)
            hijo=neatcx(of1,of2)
            hijo.descendents(0)
            hijo.fitness_sharing(0)
            del hijo.fitness.values
            r.append(hijo)
            ind1.descendents(ind1.get_descendents()-0.5)
            ind2.descendents(ind2.get_descendents()-0.5)
            if bandera==0:
                i+=1
            bandera=1
            if ind2.get_descendents()<=0:
                for xi in range(len(copy_parent)):
                    if copy_parent[xi] == ind2:
                        del copy_parent[xi]
                        break
        if ind1.get_descendents()<=0:
            for xi in range(len(copy_parent)):
                if copy_parent[xi] == ind1:
                    del copy_parent[xi]
                    break
        if bandera==0:
            i+=1
    return r

