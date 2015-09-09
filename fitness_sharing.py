from speciation import *
# tenemos que enviar una lista de parametros
#determinados, de algun punto de la iniciacion
def print_fit(population):
    for ind in population:
        print ind.fitness.values

def SpeciesPunishment(population,params):
    salvar=params[0] #params.DontPenaliza
    penalizar=params[1] #param.penalization_method
    protect=params[2] #params.sharefitness

    #Elegir el tipo de penalizacion
    for ind in population:
        if protect=='yes':
            if ind.get_specie()==None or ind.get_specie()==0:
                ind.specie(1)
                ind.penalty(True)
                ind.fitness_sharing(ind.fitness.values[0])
            #else:
            if penalizar==1:
                ind.fitness_sharing(ind.fitness.values)
            if penalizar==2:
                num_ind=get_specie_ind(ind,population)
                adj_fit=ind.fitness.values[0] * int(num_ind)
                ind.fitness_sharing(adj_fit)
            ind.penalty(True)
        elif protect=='no':
            ind.fitness_sharing(ind.fitness.values[0])
            ind.penalty(True)
    out=open('aagh.txt','a')
    for ind in population:
        out.write('\n %s %s %s %s'% (ind.get_fsharing(),ind.fitness.values, ind.get_specie(), ind))
    out.close()
    #Habra que revisar si se puede optimizar este proceso
    if salvar=='best_specie':
        id_mejor=0
        fitness_mejor=9999999999
        nodos_mejor=9999999999
        level_mejor=9999999999

        for ind, i in population, range(population):
            if ind.fitness.values<fitness_mejor:
                id_mejor=i
                fitness_mejor=ind.fitness.values
                nodos_mejor=len(ind)
                level_mejor=ind.height
            elif ind.fitness.values==fitness_mejor:
                if len(ind)<nodos_mejor:
                    id_mejor=i
                    fitness_mejor=ind.fitness.values
                    nodos_mejor=len(ind)
                    level_mejor=ind.height
                elif len(ind)==nodos_mejor:
                    if ind.height<level_mejor:
                        id_mejor=i
                        fitness_mejor=ind.fitness.values
                        nodos_mejor=len(ind)
                        level_mejor=ind.height
        if id_mejor!=0 or id_mejor!=None:
            population[id_mejor].fitness_sharing(population[id_mejor].fitness.values[0])
    elif salvar=='best_of_each_specie':
        #regresa la lista con la especie & cuantos elementos pertenecen en ella
        specie=ind_specie(population)
        id_mejor=0
        fitness_mejor=9999999999.00
        nodos_mejor=9999999999
        level_mejor=9999999999
        contador=0
        for e in specie:
            for ind, i in zip(population, range(len(population))):
                if ind.get_specie()==e[0]:
                    contador+=1
                    if ind.fitness.values[0]<fitness_mejor:
                        id_mejor=i
                        fitness_mejor=ind.fitness.values
                        nodos_mejor=len(ind)
                        level_mejor=ind.height
                    elif ind.fitness.values[0]==fitness_mejor:
                        if len(ind)<nodos_mejor:
                            id_mejor=i
                            fitness_mejor=ind.fitness.values
                            nodos_mejor=len(ind)
                            level_mejor=ind.height
                        elif len(ind)==nodos_mejor:
                            if ind.height<level_mejor:
                                id_mejor=i
                                fitness_mejor=ind.fitness.values
                                nodos_mejor=len(ind)
                                level_mejor=ind.height
                if contador==e[1]:
                    break
            lst=list(ind.fitness.values)
            lst[0]=ind.get_fsharing()
            ind.fitness.values=tuple(lst)
            if id_mejor!=0 or id_mejor!=None:
                population[id_mejor].fitness_sharing(fitness_mejor)
            #    population[id_mejor].fitness.values=fitness_mejor,