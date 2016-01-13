#add this imports
from measure_tree import *
from neat_operators import *
from speciation import *
from fitness_sharing import *
from ParentSelection import *

def eaSimple(population, toolbox, cxpb, mutpb, ngen, alg,neat, h,pelit,n_corr, p, params,stats=None,
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
    #     out.write('\n%s;%s;%s;%s;%s;%s' %(0,len(ind), ind.height, ind.get_specie(),  ind.get_fsharing(), ind))
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
    #     out.write('\n%s;%s;%s;%s;%s;%s;%s' %(0,len(ind), ind.height, ind.get_specie(), ind.fitness.values, ind.get_fsharing(), ind))
    # out.close()

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print logbook.stream

    # Begin the generational process
    for gen in range(1, ngen+1):
        # out=open('offinit_%d.txt','a')
        # for ind in population:
        #     out.write('\n%s;%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(), ind.fitness.values, ind.get_fsharing(), ind))
        # out.close()
        # Select the next generation individuals
        if alg:
            parents=p_selection(population, gen)
        else:
            parents = toolbox.select(population, len(population))

        # out=open('parents_%d.txt'%n_corr,'a')
        # for ind in parents:
        #     out.write('\n%s;%s;%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(), ind.get_descendents(),ind.fitness.values, ind.get_fsharing(), ind))
        # out.close()
        # Vary the pool of individuals
        #here will be evaluated the parents pool with
        #the neat crossover algorithm
        if neat:
            n=len(parents)
            mut=1
            cx=1
            offspring=neatGP(toolbox,parents,cxpb,mutpb,n,mut,cx,pelit)
        else:
            offspring = varAnd(parents, toolbox, cxpb, mutpb)


        # for ind in parents:
        #     out.write('\n  %s %s %s %s %s %s' %(gen,len(ind), ind.height, ind.get_specie(),  ind.get_fsharing(), ind))


        #asignar especies en cada individuo en la poblacion
        if alg:
            #realiza la especiacion de la poblacion, dado un parametro h
            #species(offspring,h)
            specie_parents_child(parents,offspring,h)
            #asigna a cada individuo de la poblacion, el numero de individuos
            #dentro de su misma especie
            # out=open('offtneat_%d.txt'%n_corr,'a')
            # for ind in offspring:
            #     out.write('\n%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(),  ind.get_fsharing(), ind))
            # out.close()
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
        #     out.write('\n%s;%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(), ind.fitness.values, ind.get_fsharing(), ind))
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

        out=open('popgen_%d_%d.txt'%(p, n_corr),'a')
        for ind in population:
            out.write('\n%s;%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(), ind.fitness.values[0], ind.get_fsharing(), ind))

    return population, logbook


def eaSimpleLS(population, toolbox, cxpb, mutpb, ngen, neat_alg, neat_cx, neat_h,neat_pelit, LS_flag, LS_select,n_corr, p, params,stats=None,
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

    # out=open('popinit.txt','a')
    # for ind in population:
    #     out.write('\n  %s %s %s %s %s; %s' %(0,len(ind), ind.height, ind.get_specie(),  ind.get_fsharing(), ind))
    # out.close()

    #asignar especies en cada individuo en la poblacion
    if neat_alg:
        #realiza la especiacion de la poblacion, dado un parametro h
        species(population,neat_h)
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
    if neat_alg:
        SpeciesPunishment(population,params,neat_h)

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
        if neat_alg:
            parents=p_selection(population, gen)
        else:
            offspring = toolbox.select(population, len(population))

        # out=open('parents.txt','a')
        # for ind in parents:
        #     out.write('\n%s;%s;%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(), ind.get_descendents(),ind.fitness.values, ind.get_fsharing(), ind))
        # out.close()
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

        # out=open('aftneat.txt','a')
        # for ind in parents:
        #     out.write('\n  %s %s %s %s %s %s' %(gen,len(ind), ind.height, ind.get_specie(),  ind.get_fsharing(), ind))
        # for ind in offspring:
        #     out.write('\n  %s %s %s %s %s %s' %(gen,len(ind), ind.height, ind.get_specie(),  ind.get_fsharing(), ind))
        # out.close()

        #asignar especies en cada individuo en la poblacion
        if neat_alg:
            #realiza la especiacion de la poblacion, dado un parametro h
            #species(offspring,h)
            specie_parents_child(parents,offspring, neat_h)
            #asigna a cada individuo de la poblacion, el numero de individuos
            #dentro de su misma especie
            # out=open('aftneat.txt','a')
            # for ind in offspring:
            #     out.write('\n%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(),  ind.get_fsharing(), ind))
            # out.close()
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

        if neat_alg:
            SpeciesPunishment(offspring,params, neat_h)

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
            #agregar las otras dos heuristicas
            ###1.Los mejores de cada especie.
            ###2.La heuristica de LS por cada grupo de especie.
            #por lo tanto necesito sacar el tamano promedio de la poblacion
            n_nodes=[]
            for ind in population:
               n_nodes.append(len(ind))
            nn_nodes=np.asarray(n_nodes)
            av_size=np.mean(nn_nodes)
            c=1.5
            for ind in population:
                ind.LS_probability(0.)
                y=c-(len(ind)/av_size)
                if y>1.:
                    ps=1
                    ind.LS_probability(1.)
                elif (y>=0. and y<=1.):
                    ps=y
                    ind.LS_probability(y)

            if random.random()<ind.get_LS_prob():
                #print 'hey'
                strg=ind.__str__()
                l_strg=add_subt(strg)
                c = tree2f()
                cd=c.convert(l_strg)
                print cd
                c2=tree2f()
                cd2=c2.convert_r(l_strg)
                print cd2
                #falta extraer la lista de parametros o decidir no enviarsela
                #extraer la funcion, en este caso la expresion del arbol indicandole los parametros
                #como agregar los parametros
                xdata=np.linspace(0,5,20)
                direccion="./data_corridas/Koza/corrida1/test_y.txt"
                ydata = np.genfromtxt(direccion, delimiter=' ')
                #curve_fit_2(eval_, cd, xdata, ydata, p0=p, full_output=1)
                beta_opt, beta_cov, info, msg, success= curve_fit_2(eval_,cd , xdata, ydata, p0=ind.params ,full_output=1)
                print('number of function calls =', info['nfev'])
                print msg
                print beta_opt

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print logbook.stream

        out=open('popgen_%d_%d.txt'%(p,n_corr),'a')
        for ind in population:
            out.write('\n%s;%s;%s;%s;%s;%s;%s;%s' %(gen,len(ind), ind.height, ind.get_specie(), ind.fitness.values[0], ind.get_fsharing(), ind.fitness_test.values[0], ind))
    return population, logbook
