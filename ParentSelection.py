from deap import gp
from speciation import *
class p_selection():
    #debe de recibir de entrada el parametro de
    #survival_thershold=0.5
    def p_selection(self, population):
        #provisional
        survival=0.5
        #sacar promedio para penalizar
        prom_ap_penal=avg(population)
        #penalizar al promedio
        if prom_ap_penal>10:
            prom_ap_penal=10
        q=list()
        #conseguimos y aplicamos el num. de desc.
        # a cada individuo
        for ind in population:
            ind.descendent(num_desc(ind, prom_ap_penal))

        numbest=round(len(population)*survival)
        q=population

        #ordenar poblacion por su fitness
        allpotfit=sort_fitness(q)
        #obtener numero de especies
        specie=ind_specie(population)
        for e in specie:
            contador=0
            for ind in population:
                if ind.get_specie()==e[0]:
                    contador+=1
                    if round(ind.get_numspecie() * survival)<contador:
                        ind.fitness.values=9999999
                        if ind.get_numspecie==contador:
                            break



def num_desc(self, ind, avg):
    numd=round(avg/ind.get_fsharing())
    return numd


def avg(self, population):
    suma=0
    for ind in population:
        suma+=ind.get_fsharing()
    promedio=suma/len(population)
    return promedio

def sort_fitness(population):
    allpotfit=list()
    orderbyfit=list()
    for ind in population:
        allpotfit.append([ind, ind.fitness.values, ind.get_fsharing])
    orderbyfit=sorted(allpotfit, key=lambda ind: ind[1])
    return orderbyfit