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
        if n>len(parents):
            lim=int(round(n/len(parents)))
            for d in range(lim):
                copy_parent+=parents
        eflag=int(round(random.random()))
        if eflag:
            ind1=copy_parent[0] #el mejor individuo debido su fitnes
        else:
            ind1=random.choice(copy_parent)
        if random.random()<mutpb:
            of=copy.deepcopy(ind1)
            offspring=toolbox.mutate(of)
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
            r.append(hijo)
            ind1.descendents(ind1.get_descendents()-0.5)
            ind2.descendents(ind2.get_descendents()-0.5)
            i+=1
            if ind2.get_descendents()<=0:
                for i in range(len(copy_parent)):
                    if copy_parent[i] == ind2:
                        del copy_parent[i]
                        break
        if ind1.get_descendents()<=0:
            for i in range(len(copy_parent)):
                if copy_parent[i] == ind1:
                    del copy_parent[i]
                    break
    return r

