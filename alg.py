def eaSimple(population, toolbox, cxpb, mutpb, ngen, neat, neatcx, h,pelit,n_corr, problem, params,stats=None,
             halloffame=None, verbose=__debug__):
    """This algorithm reproduce the simplest evolutionary algorithm as
    presented in chapter 7 of [Back2000]_.

    :param population: A list of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    ## Modify by Perla Juarez
    :param ngen: The number of generation.
    :param neat: wheter or not to use neatGP
    :param neatcx: wheter or not to use neat-crossover
    :param h: indicate the distance allowed between each specie
    :param pelit: indicate the distance allowed between each specie
    :param n_corr: indicate the number of run
    :param problem: indicate the number of problem that you are running (menu)
    :param params:indicate the params for the fitness sharing, the diffetent
                    options are:
                    -DontPenalize(str): 'best_specie' or 'best_of_each_specie'
                    -Penalization_method(int):
                        1.without penalization
                        2.penalization fitness sharing
                        3.new penalization
                    -ShareFitness(str): 'yes' or 'no'
    ##
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

    if neat:  # assign species to each individual on the population
        species(population, h)  # h is the parameter for the dissimilarity
        ind_specie(population)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    fitnesses_test = toolbox.map(toolbox.evaluate_test, invalid_ind)
    for ind, fit, fit_test in zip(invalid_ind, fitnesses, fitnesses_test):
        ind.fitness.values = fit
        ind.fitness_test.values = fit_test

    if neat:
        SpeciesPunishment(population,params,h)

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print logbook.stream

    # Begin the generational process
    for gen in range(1, ngen+1):
        if neat:
            parents = p_selection(population, gen)
        else:
            parents = toolbox.select(population, len(population))

        # Vary the pool of individuals
        # here will be evaluated the parents pool with
        # the neat crossover algorithm
        if neatcx:
            n = len(parents)
            mut = 1  # 1. Activate mutation - Otherwise. Deactivate mutaction
            cx = 1  # 1. Activate crossover - Otherwise. Deactivate crossover
            offspring = neatGP(toolbox,parents,cxpb,mutpb,n,mut,cx,pelit)
        else:
            offspring = varAnd(parents, toolbox, cxpb, mutpb)

        if neat:  # assigne the specie to each offspring
            specie_parents_child(parents, offspring, h)
            offspring[:] = parents+offspring
            ind_specie(offspring)

        for ind in offspring:
            del ind.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        fitnesses_test = toolbox.map(toolbox.evaluate_test, invalid_ind)
        for ind, fit, fit_test in zip(invalid_ind, fitnesses, fitnesses_test):
            ind.fitness.values = fit
            ind.fitness_test.values = fit_test

        if neat:
            SpeciesPunishment(offspring,params,h)

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        # the best offsprings in R replace the pworst% individual
        # of the population P
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print logbook.stream
        if neat:
            out = open('popgen_%d_%d.txt'%(p,n_corr),'a')
            for ind in population:
                out.write('\n%s;%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(), ind.fitness.values, ind.get_fsharing(), ind))
        else:
            out = open('popgen_%d_%d.txt'%(p,n_corr),'a')
            for ind in population:
                out.write('\n%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.fitness.values, ind))

    return population, logbook
