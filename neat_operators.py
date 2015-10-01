#Variacion de los individuos
#Aplicar lo operadores
#los individuos padres provienen de un algoritmo
#especial, donde se seleccionan los mejores de cada especie
#las probabilidades de cruce y mutacion, son las mismas
#que se manejan en todos los algoritmos.
#n es el numero de hijos descendientes que se espera que regrese
#la clase, este parametro podria ser omitido
import random
#from neat_gp import *
from ParentSelection import sort_fitnessvalues
from speciation import get_specie_ind, ind_specie
from crosspoints import *
def neatGP(toolbox,parents,cxpb,mutpb,n, mut,cx):
    r=list()
    i=0
    copy_parent=copy.deepcopy(parents)

    while i<n:
        uout=open('parentscopy.txt','a')
        if n>len(copy_parent):
            lim=int(round(n/len(copy_parent)))
            for d in range(lim):
                uout.write('\n++++')
                copy_parent+=copy_parent

        for ind in copy_parent:
            uout.write('\n %s %s'%(ind.get_specie(), ind))
        uout.write('\n----')
        uout.close()
        eflag=int(round(random.random()))
        if eflag:
            ind1=copy_parent[0] #el mejor individuo debido su fitness
        else:
            ind1=random.choice(copy_parent)
        if mut==1 and random.random()<mutpb:#
            of=copy.deepcopy(ind1)
            offspring=toolbox.mutate(of)
            offspring[0].descendents(0)
            offspring[0].fitness_sharing(0)
            offspring[0].specie(None)
            del offspring[0].fitness.values

            if i<n:
                r.append(offspring[0])
                i+=1
            else:
                break

            ind1.descendents(ind1.get_descendents()-1)
        elif cx==1:
            out=open('neatcx.txt','a')
            out.write('\n ind:%s'%(ind1))
            ind_nspecie=get_specie_ind(ind1,copy_parent)
            if ind_nspecie > 1:
                out.write('\n num_specie:%s'%(ind_nspecie))
                for q in range(len(copy_parent)):
                    if copy_parent[q].get_specie() == ind1.get_specie() and copy_parent[q]!=ind1:
                        ind2 = copy_parent[q]
                        break
                    else:
                        #elitista
                        try:
                            ind2=elitism_choice(ind1, copy_parent)
                        except:
                        #al azar
                            ind2 = random.choice(copy_parent)
            else:
                ind2 = random.choice(copy_parent)
            out.write('\n ind2:%s'%(ind2))
            of1 = copy.deepcopy(ind1)
            of2 = copy.deepcopy(ind2)
            hijo = neatcx(of1, of2)
            out.write('\nhijo:%s' %(hijo))
            out.close()
            hijo.descendents(0)
            hijo.fitness_sharing(0)
            hijo.specie(None)
            del hijo.fitness.values

            if i < n:
                r.append(hijo)
                i += 1
            else:
                break

            ind1.descendents(ind1.get_descendents() - 0.5)
            ind2.descendents(ind2.get_descendents() - 0.5)

            if ind2.get_descendents() <= 0:
                for xi in range(len(copy_parent)):
                    if copy_parent[xi] == ind2:
                        del copy_parent[xi]
                        break
        if ind1.get_descendents()<=0:
            for xi in range(len(copy_parent)):
                if copy_parent[xi] == ind1:
                    del copy_parent[xi]
                    break
    return r

def elitism_choice(ind, parents):
    #species=ind_specie(parents)
    sort_par=sort_fitnessvalues(parents)
    for i in range(len(sort_par)):
        if sort_par[i]!=ind:
            ind2=sort_par[i]
            break
    return ind2