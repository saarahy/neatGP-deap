from deap import gp
from speciation import *
#debe de recibir de entrada el parametro de
    #survival_thershold=0.5
class p_selection():
    def p_selection(self, population):
        #provisional
        survival=0.5
        #sacar promedio para penalizar
        prom_ap_penal=avg(population)
        #penalizar al promedio
        if prom_ap_penal>10:
            prom_ap_penal=10


        #conseguimos y aplicamos el num. de desc.
        # a cada individuo
        for ind in population:
            ind.descendent(num_desc(ind, prom_ap_penal))

        q=population

        #obtener numero de especies
        specie=ind_specie(q)
        #crear grupos auxilares
        gpo_specie=list()
        parents=list()

        for e in specie:
            for ind in q:
                if ind.get_specie()==e[0]:
                    gpo_specie.append(ind)
            parents.append(eliminar_ind(gpo_specie,survival))




def num_desc(self, ind, avg):
    numd=round(avg/ind.fitness.values)
    return numd


def avg(self, population):
    suma=0
    for ind in population:
        suma+=ind.fitness.values
    promedio=suma/len(population)
    return promedio

def sort_fitness(population):
    allpotfit=list()
    orderbyfit=list()
    for ind in population:
        allpotfit.append([ind, ind.fitness.values, ind.get_fsharing])
    orderbyfit=sorted(allpotfit, key=lambda ind: ind[2])
    return orderbyfit

def eliminar_ind(gpo_specie, survival):
    sort_gpo=sort_fitness(gpo_specie)
    indice=int(round(len(sort_gpo)-(len(sort_gpo)*survival)))
    reverse_gpo=sorted(sort_gpo, reverse=True)
    for i in range(indice):
        del reverse_gpo[0]
    sort_gpo=sort_fitness(reverse_gpo)
    return sort_gpo
