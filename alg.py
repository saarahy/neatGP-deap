import random
import tools
import time
import funcEval
from measure_tree import *
from neat_operators import *
from speciation import *
from fitness_sharing import *
from ParentSelection import *
from tree_subt import add_subt
from scipy.optimize.minpack import curve_fit_2
from tree2func import tree2f
from eval_str import eval_
from treesize_h import trees_h,specie_h,best_specie
from tree_subt import add_subt_cf


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
            offspring[i-1].bestspecie_set(0), offspring[i].bestspecie_set(0)
            offspring[i-1].LS_applied_set(0), offspring[i].LS_applied_set(0)
    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values
            offspring[i].descendents(0)
            offspring[i].fitness_sharing(0)
            offspring[i].specie(None)
            offspring[i].bestspecie_set(0)
            offspring[i].LS_applied_set(0)
    return offspring

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

    if funcEval.LS_flag:
        for ind in population:
            sizep=len(ind)+2
            ind.params_set(np.ones(sizep))
            param=ind.get_params()

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
    if funcEval.LS_flag:
            out=open('popgen_%d_%d.txt'%(num_p,n_corr),'a')
            for ind in population:
                strg=ind.__str__() #convierte en str el individuo
                l_strg=add_subt_cf(strg, args=[]) #le anade el arbol y lo convierte en arreglo
                c = tree2f() #crea una instancia de tree2f
                cd=c.convert(l_strg) #convierte a l_strg en infijo
                out.write('\n%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' %(0,funcEval.cont_evalp,len(ind), ind.height, ind.get_specie(), ind.bestspecie_get(), ind.LS_applied_get(),ind.fitness.values[0], ind.get_fsharing(), ind.fitness_test.values[0], ind.LS_fitness_get(),ind.get_params(),cd,ind))
            print funcEval.cont_evalp
    else:
            out=open('popgen_%d_%d.txt'%(num_p,n_corr),'a')
            for ind in population:
                out.write('\n%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' %(0,funcEval.cont_evalp,len(ind), ind.height, ind.get_specie(), ind.bestspecie_get(), ind.LS_applied_get(),ind.fitness.values[0], ind.get_fsharing(), ind.fitness_test.values[0], ind.LS_fitness_get(),ind))
    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print logbook.stream

    # Begin the generational process
    #modificar para el numero de evaluaciones de la funcion objetivo
    for gen in range(1, ngen+1):

        if funcEval.cont_evalp > cont_evalf:
            break
        # Select the next generation individuals
        if neat_alg:
            parents=p_selection(population, gen)
        else:
            parents = toolbox.select(population, len(population))


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
        if funcEval.LS_flag:
            new_invalid_ind=[]
            for ind in invalid_ind:
                strg=ind.__str__() #convierte en str el individuo
                l_strg=add_subt(strg, ind) #le anade el arbol y lo convierte en arreglo
                c = tree2f() #crea una instancia de tree2f
                cd=c.convert(l_strg) #convierte a l_strg en infijo
                new_invalid_ind.append(cd)
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            fitness_ls= toolbox.map(toolbox.evaluate, new_invalid_ind)
            fitnesses_test = toolbox.map(toolbox.evaluate_test, invalid_ind)
            for ind, fit, fit_test, ls_fit in zip(invalid_ind, fitnesses, fitnesses_test,fitness_ls):
                if np.isinf(ls_fit) or np.isinf(ls_fit) or np.isnan(ls_fit):
                    funcEval.cont_evalp=funcEval.cont_evalp+1
                    ind.fitness.values = fit
                    ind.fitness_test.values = fit_test
                    ind.LS_fitness_set(ls_fit[0])
                else:
                    funcEval.cont_evalp=funcEval.cont_evalp+1
                    ind.fitness.values = ls_fit
                    ind.fitness_test.values = fit_test
                    ind.LS_fitness_set(fit[0])
        else:
            #invalid_ind = [ind for ind in population if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            fitnesses_test=toolbox.map(toolbox.evaluate_test, invalid_ind)
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
                trees_h(population, n_corr, pset)
            elif LS_select==2:
                best_specie(population, n_corr,pset)
            else:
                specie_h(population, n_corr, pset)


            new_invalid_ind=[]
            for ind in invalid_ind:
                if ind.LS_applied_get():
                    strg=ind.__str__() #convierte en str el individuo
                    l_strg=add_subt(strg, ind) #le anade el arbol y lo convierte en arreglo
                    c = tree2f() #crea una instancia de tree2f
                    cd=c.convert(l_strg) #convierte a l_strg en infijo
                    new_invalid_ind.append(cd)
            invalid_ind = [ind for ind in offspring if ind.LS_applied_get()]
            fitness_ls= toolbox.map(toolbox.evaluate, new_invalid_ind)
            for ind,ls_fit in zip(invalid_ind,fitness_ls):
                if np.isinf(ls_fit) or np.isinf(ls_fit) or np.isnan(ls_fit):
                    funcEval.cont_evalp=funcEval.cont_evalp+1
                    ind.LS_fitness_set(ls_fit[0])
                else:
                    funcEval.cont_evalp=funcEval.cont_evalp+1
                    ind.LS_fitness_set(ind.fitness.values[0])
                    ind.fitness.values=ls_fit

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(population), **record)
        if verbose:
            print logbook.stream

        if funcEval.LS_flag:
            #out=open('popgen_%d_%d.txt'%(num_p,n_corr),'a')
            for ind in population:
                strg=ind.__str__() #convierte en str el individuo
                l_strg=add_subt_cf(strg, args=[]) #le anade el arbol y lo convierte en arreglo
                c = tree2f() #crea una instancia de tree2f
                cd=c.convert(l_strg) #convierte a l_strg en infijo
                out.write('\n%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' %(gen,funcEval.cont_evalp,len(ind), ind.height, ind.get_specie(), ind.bestspecie_get(), ind.LS_applied_get(),ind.fitness.values[0], ind.get_fsharing(), ind.fitness_test.values[0], ind.LS_fitness_get(),ind.get_params(),cd,ind))
            print funcEval.cont_evalp
        else:
            #out=open('popgen_%d_%d.txt'%(num_p,n_corr),'a')
            for ind in population:
                out.write('\n%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' %(gen,funcEval.cont_evalp,len(ind), ind.height, ind.get_specie(), ind.bestspecie_get(), ind.LS_applied_get(),ind.fitness.values[0], ind.get_fsharing(), ind.fitness_test.values[0], ind.LS_fitness_get(),ind))
    return population, logbook
