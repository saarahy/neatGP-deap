#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

import random
import operator
import csv
import itertools

import numpy as np

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
import my_operators as mo

direccion="./data_corridas/BreastCancer/breast-cancer-wisconsin.txt"
with open(direccion) as spambase:
    # spamReader = csv.reader(spambase)
    # spam = list(list(elem for elem in row) for row in spamReader)
    spamReader = csv.reader(spambase,  delimiter=',', skipinitialspace=True)
    num_c = sum(1 for line in open(direccion))
    num_r = len(next(csv.reader(open(direccion), delimiter=',', skipinitialspace=True)))
    Matrix = np.empty((num_r, num_c,))
    for row, c in zip(spamReader, range(num_c)):
        for r in range(num_r):
            try:
                #print row[r]
                Matrix[r, c] = row[r]
            except ValueError:
                print 'Line {r} is corrupt' , r
                break

# defined a new primitive set for strongly typed GP
pset = gp.PrimitiveSet("MAIN", 10)

# boolean operators
# pset.addPrimitive(operator.and_, [bool, bool], bool)
# pset.addPrimitive(operator.or_, [bool, bool], bool)
# pset.addPrimitive(operator.not_, [bool], bool)

# floating point operators
# Define a protected division function
def protectedDiv(left, right):
    try: return left / right
    except ZeroDivisionError: return 1
# Define a new if-then-else function
def if_then_else(input, output1, output2):
    if input: return output1
    else: return output2

pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(np.sin, 1)
pset.addPrimitive(np.cos, 1)
pset.addPrimitive(mo.mysqrt, 1)
pset.addPrimitive(np.abs, 1)
pset.addPrimitive(if_then_else, 3)
pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5' , ARG6='x6' , ARG7='x7' , ARG8='x8' , ARG9='x9')
#pset.addPrimitive(operator.lt, [float, float], bool)
# pset.addPrimitive(operator.eq, [float, float], bool)
# pset.addPrimitive(if_then_else, [bool, float, float], float)

# terminals
# pset.addEphemeralConstant("rand100", lambda: random.random() * 100)
# pset.addTerminal(False)
# pset.addTerminal(True)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("FitnessTest", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, fitness_test=creator.FitnessTest)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalSpambase(individual):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Randomly sample 400 mails in the spam database
    spam_samp = random.sample(Matrix.T, 400)
    # Evaluate the sum of correctly identified mail as spam
    result = sum(bool(func(*mail[:10])) is bool(mail[10]) for mail in spam_samp)
    return result,
    
toolbox.register("evaluate", evalSpambase)
toolbox.register("evaluate_test", evalSpambase)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    #random.seed(10)
    pop = toolbox.population(n=200)
    hof = tools.HallOfFame(1)
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    stats_fit_test = tools.Statistics(lambda i: i.fitness_test.values)
    mstats = tools.MultiStatistics(fitness=stats_fit,size=stats_size, fitness_test=stats_fit_test)
    mstats.register("avg", np.mean)
    mstats.register("std", np.std)
    mstats.register("min", np.min)
    mstats.register("max", np.max)

    params = ['best_of_each_specie', 2, 'yes']
    neatcx = True
    neat = True
    pelit = 0.5
    n_corr=1
    p=1
    algorithms.eaSimple(pop, toolbox, 0.7, 0.3, 100, neat, neatcx, 0.15, pelit, n_corr, p, params, stats=mstats, halloffame=hof, verbose=True)

    return pop, mstats, hof

if __name__ == "__main__":
    main()
