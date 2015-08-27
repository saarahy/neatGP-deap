# tenemos que enviar una lista de parametros
#determinados, de algun punto de la iniciacion
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
            else:
                if penalizar==1:
                    ind.fitness(ind.fitness)
                if penalizar==2:
                     adj_fit=ind.fitness_sin_penalizar*ind.get_specie()
                     ind.fitness(adj_fit)
            ind.penalty(True)
        elif protect=='no':
            ind.fitness(ind.fitness)
            ind.penalty(True)

