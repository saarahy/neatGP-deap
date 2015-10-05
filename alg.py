def varAnd(population, toolbox, cxpb, mutpb):
    """Part of an evolutionary algorithm applying only the variation part
    (crossover **and** mutation). The modified individuals have their
    fitness invalidated. The individuals are cloned so returned population is
    independent of the input population.

    :param population: A list of individuals to vary.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :returns: A list of varied individuals that are independent of their
              parents.

    The variation goes as follow. First, the parental population
    :math:`P_\mathrm{p}` is duplicated using the :meth:`toolbox.clone` method
    and the result is put into the offspring population :math:`P_\mathrm{o}`.
    A first loop over :math:`P_\mathrm{o}` is executed to mate consecutive
    individuals. According to the crossover probability *cxpb*, the
    individuals :math:`\mathbf{x}_i` and :math:`\mathbf{x}_{i+1}` are mated
    using the :meth:`toolbox.mate` method. The resulting children
    :math:`\mathbf{y}_i` and :math:`\mathbf{y}_{i+1}` replace their respective
    parents in :math:`P_\mathrm{o}`. A second loop over the resulting
    :math:`P_\mathrm{o}` is executed to mutate every individual with a
    probability *mutpb*. When an individual is mutated it replaces its not
    mutated version in :math:`P_\mathrm{o}`. The resulting
    :math:`P_\mathrm{o}` is returned.

    This variation is named *And* beceause of its propention to apply both
    crossover and mutation on the individuals. Note that both operators are
    not applied systematicaly, the resulting individuals can be generated from
    crossover only, mutation only, crossover and mutation, and reproduction
    according to the given probabilities. Both probabilities should be in
    :math:`[0, 1]`.
    """
    offspring = [toolbox.clone(ind) for ind in population]

    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i-1], offspring[i] = toolbox.mate(offspring[i-1], offspring[i])
            del offspring[i-1].fitness.values, offspring[i].fitness.values
            offspring[i-1].descendents(0), offspring[i].descendents(0)
            offspring[i-1].fitness_sharing(0), offspring[i].fitness_sharing(0)
            offspring[i-1].specie(None), offspring[i].specie(None)

    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values
            offspring[i].descendents(0)
            offspring[i].fitness_sharing(0)
            offspring[i].specie(None)

    return offspring

def eaSimple(population, toolbox, cxpb, mutpb, ngen, alg,neat, h,n_corr, params,stats=None,
             halloffame=None, verbose=__debug__):
    """This algorithm reproduce the simplest evolutionary algorithm as
    presented in chapter 7 of [Back2000]_.

    :param population: A list of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :param ngen: The number of generation.
    :param neat: wheter or not to use neatGP
    :param h: indicate the distance allowed between each specie
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

    # out=open('popinit.txt','a')
    # for ind in population:
    #     out.write('\n  %s %s %s %s %s; %s' %(0,len(ind), ind.height, ind.get_specie(),  ind.get_fsharing(), ind))
    # out.close()

    #asignar especies en cada individuo en la poblacion
    if alg:
        #realiza la especiacion de la poblacion, dado un parametro h
        species(population,h)
        #asigna a cada individuo de la poblacion, el numero de individuos
        #dentro de su misma especie
        ind_specie(population)

    # out=open('popinitspecie.txt','a')
    # for ind in population:
    #     out.write('\n  %s %s %s %s %s %s' %(0,len(ind), ind.height, ind.get_specie(),  ind.get_fsharing(), ind))
    # out.close()

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    fitnesses_test=toolbox.map(toolbox.evaluate_test, invalid_ind)
    for ind, fit, fit_test in zip(invalid_ind, fitnesses, fitnesses_test):
        ind.fitness.values = fit
        ind.fitness_test.values = fit_test

    # out=open('popbefpen.txt','a')
    # for ind in population:
    #     out.write('\n  %s %s %s %s %s %s %s' %(0,len(ind), ind.height, ind.get_specie(), ind.fitness.values, ind.get_fsharing(), ind))
    # out.close()

    #modificar aptitud en base al fitness sharing y la penalizacion
    #dependiendo del parametro
    if alg:
        SpeciesPunishment(population,params,h)

    # out=open('popaftpen.txt','a')
    # for ind in population:
    #     out.write('\n  %s %s %s %s %s %s %s' %(0,len(ind), ind.height, ind.get_specie(), ind.fitness.values, ind.get_fsharing(), ind))
    # out.close()

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print logbook.stream

    # Begin the generational process
    for gen in range(1, ngen+1):
        # out=open('offinit.txt','a')
        # for ind in population:
        #     out.write('\n%s;%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(), ind.fitness.values, ind.get_fsharing(), ind))
        # out.close()
        # Select the next generation individuals
        if alg:
            parents=p_selection(population)
        else:
            offspring = toolbox.select(population, len(population))

        # out=open('parents.txt','a')
        # for ind in parents:
        #     out.write('\n  %s %s %s %s %s %s %s' %(gen,len(ind), ind.height, ind.get_specie(), ind.fitness.values, ind.get_fsharing(), ind))
        # out.close()
        # Vary the pool of individuals
        #here will be evaluated the parents pool with
        #the neat crossover algorithm
        if neat:
            n=len(parents)
            mut=1
            cx=1
            offspring=neatGP(toolbox,parents,cxpb,mutpb,n,mut,cx)
        else:
            offspring = varAnd(parents, toolbox, cxpb, mutpb)

        # out=open('aftneat.txt','a')
        # for ind in parents:
        #     out.write('\n  %s %s %s %s %s %s' %(gen,len(ind), ind.height, ind.get_specie(),  ind.get_fsharing(), ind))
        # for ind in offspring:
        #     out.write('\n  %s %s %s %s %s %s' %(gen,len(ind), ind.height, ind.get_specie(),  ind.get_fsharing(), ind))
        # out.close()

        #asignar especies en cada individuo en la poblacion
        if alg:
            #realiza la especiacion de la poblacion, dado un parametro h
            #species(offspring,h)
            specie_parents_child(parents,offspring,h)
            #asigna a cada individuo de la poblacion, el numero de individuos
            #dentro de su misma especie
            offspring[:]=parents+offspring
            ind_specie(offspring)



        # out=open('aftspecie.txt','a')
        # for ind in offspring:
        #     out.write('\n  %s %s %s %s %s %s' %(gen,len(ind), ind.height, ind.get_specie(), ind.get_fsharing(), ind))
        # out.close()

        for ind in offspring:
            del ind.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        fitnesses_test = toolbox.map(toolbox.evaluate_test, invalid_ind)
        for ind, fit, fit_test in zip(invalid_ind, fitnesses, fitnesses_test):
            ind.fitness.values = fit
            ind.fitness_test.values = fit_test

        # out=open('offbefpen.txt','a')
        # for ind in offspring:
        #     out.write('\n  %s %s %s %s %s %s %s' %(gen,len(ind), ind.height, ind.get_specie(), ind.fitness.values, ind.get_fsharing(), ind))
        # out.close()

        if alg:
            SpeciesPunishment(offspring,params,h)

        # out=open('offaftpen.txt','a')
        # for ind in offspring:
        #     out.write('\n  %s %s %s %s %s %s %s' %(gen,len(ind), ind.height, ind.get_specie(), ind.fitness.values, ind.get_fsharing(), ind))
        # out.close()

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        #the best offsprings in R replace the pworst% individual
        #of the population P
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print logbook.stream

        out=open('popgen_%d.txt'%n_corr,'a')
        for ind in population:
            out.write('\n%s;%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(), ind.fitness.values, ind.get_fsharing(), ind))

    return population, logbook
