#add this imports
from measure_tree import *
from neat_operators import *
from speciation import *
from fitness_sharing import *
from ParentSelection import *

def eaSimple(population, toolbox, cxpb, mutpb, ngen, neat_alg, neat_cx, neat_h,neat_pelit, LS_flag, LS_select, cont_evalf,pset,n_corr, num_p, params,stats=None,
             halloffame=None, verbose=__debug__):
    """This algorithm reproduce the simplest evolutionary algorithm as
    presented in chapter 7 of [Back2000]_.

    :param population: A list of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :param ngen: The number of generation.
    :param neat_alg: wheter or not to use species stuff.
    :param neat_cx: wheter or not to use neatGP cx
    :param neat_h: indicate the distance allowed between each specie
    :param neat_pelit: probability of being elitist, it's used in the neat cx and mutation
    :param LS_flag: wheter or not to use LocalSearchGP
    :param LS_select: indicate the kind of selection to use the LSGP on the population.
    :param cont_evalf: contador maximo del numero de evaluaciones
    :param n_corr: run number just to wirte the txt file
    :param p: problem number just to wirte the txt file
    :param params:indicate the params for the fitness sharing, the diffetent
                    options are:
                    -DontPenalize(str): 'best_specie' or 'best_of_each_specie'
                    -Penalization_method(int):
                        1.without penalization
                        2.penalization fitness sharing
                        3.new penalization
                    -ShareFitness(str): 'yes' or 'no'
    :param stats: A :class:`~deap.tools.Statistics` object that is updated
                  inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :returns: The final population.

    It uses :math:`\lambda = \kappa = \mu` and goes as follow.
    It first initializes the population (:math:`P(0)`) by evaluating
    every individual presenting an invalid fitness. Then, it enters the
    evolution loop that begins by the selection of the :math:`P(g+1)`
    population. Then the crossover operator is applied on a proportion of
    :math:`P(g+1)` according to the *cxpb* probability, the resulting and the
    untouched individuals are placed in :math:`P'(g+1)`. Thereafter, a
    proportion of :math:`P'(g+1)`, determined by *mutpb*, is
    mutated and placed in :math:`P''(g+1)`, the untouched individuals are
    transferred :math:`P''(g+1)`. Finally, those new individuals are evaluated
    and the evolution loop continues until *ngen* generations are completed.
    Briefly, the operators are applied in the following order ::

        evaluate(population)
        for i in range(ngen):
            offspring = select(population)
            offspring = mate(offspring)
            offspring = mutate(offspring)
            evaluate(offspring)
            population = offspring

    This function expects :meth:`toolbox.mate`, :meth:`toolbox.mutate`,
    :meth:`toolbox.select` and :meth:`toolbox.evaluate` aliases to be
    registered in the toolbox.

    .. [Back2000] Back, Fogel and Michalewicz, "Evolutionary Computation 1 :
       Basic Algorithms and Operators", 2000.
    """

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    #asignar especies en cada individuo en la poblacion
    if neat_alg:
        #realiza la especiacion de la poblacion, dado un parametro h
        species(population,neat_h)
        #asigna a cada individuo de la poblacion, el numero de individuos
        #dentro de su misma especie
        ind_specie(population)


    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    fitnesses_test=toolbox.map(toolbox.evaluate_test, invalid_ind)
    for ind, fit, fit_test in zip(invalid_ind, fitnesses, fitnesses_test):
        funcEval.cont_evalp=funcEval.cont_evalp+1
        ind.fitness.values = fit
        ind.fitness_test.values = fit_test

    #modificar aptitud en base al fitness sharing y la penalizacion
    #dependiendo del parametro
    if neat_alg:
        SpeciesPunishment(population,params,neat_h)

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print logbook.stream

    # Begin the generational process
    #modificar para el numero de evaluaciones de la funcion objetivo
    for gen in range(1, ngen+1):
        #break
        if funcEval.cont_evalp > cont_evalf:
            break
        # Select the next generation individuals
        if neat_alg:
            parents=p_selection(population, gen)
        else:
            offspring = toolbox.select(population, len(population))


        # Vary the pool of individuals
        #here will be evaluated the parents pool with
        #the neat crossover algorithm
        if neat_cx:
            n=len(parents)
            mut=1
            cx=1
            offspring=neatGP(toolbox,parents,cxpb,mutpb,n,mut,cx,neat_pelit)
        else:
            offspring = varAnd(parents, toolbox, cxpb, mutpb)

        #asignar especies en cada individuo en la poblacion
        if neat_alg:
            #realiza la especiacion de la poblacion, dado un parametro h
            #species(offspring,h)
            specie_parents_child(parents,offspring, neat_h)
            #asigna a cada individuo de la poblacion, el numero de individuos
            #dentro de su misma especie
            offspring[:]=parents+offspring
            ind_specie(offspring)

        for ind in offspring:
            del ind.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        fitnesses_test = toolbox.map(toolbox.evaluate_test, invalid_ind)
        for ind, fit, fit_test in zip(invalid_ind, fitnesses, fitnesses_test):
            funcEval.cont_evalp=funcEval.cont_evalp+1
            ind.fitness.values = fit
            ind.fitness_test.values = fit_test


        if neat_alg:
            SpeciesPunishment(offspring,params, neat_h)

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        #the best offsprings in R replace the pworst% individual
        #of the population P
        population[:] = offspring

        if LS_flag:
            #seleccionar a los individuos
            #como selecciono a los individuos
            #para eso era la heuristica
            """ LS method is applied stochastically for each tree, based on a probability
                determined by the tree size (number of nodes) and the average size of the population
                mandarle a curve_fit los parametros y la funcion
                        y=c-(s/as) if 0<=y<=1
                p(s)=   1          if y>1
                        0          otherwise
            """
            #LS_select
            ###1. HEuristica por numero de nodos
            ###2.Los mejores de cada especie.
            ###3.La heuristica de LS por cada grupo de especie.
            #por lo tanto necesito sacar el tamano promedio de la poblacion
            if LS_select==1:
                trees_h(population)
            elif LS_select==2:
                best_specie(population)
            else:
                specie_h(population)

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print logbook.stream

        out=open('popgen_%d_%d.txt'%(num_p,n_corr),'a')
        for ind in population:
            out.write('\n%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(), ind.bestspecie_get(), ind.LS_applied_get(),ind.fitness.values[0], ind.get_fsharing(), ind.fitness_test.values[0], ind))
    return population, logbook