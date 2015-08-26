from deap import base, creator, tools,gp
from speciation import *
import math

import operator
pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.renameArguments(ARG0='x')

creator.create("Individual", gp.PrimitiveTree)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalSymbReg(individual, points):
    func = toolbox.compile(expr=individual)
    sqerrors = ((func(x) - x**4 - x**3 - x**2 - x)**2 for x in points)
    return math.fsum(sqerrors) / len(points),

toolbox.register("evaluate", evalSymbReg, points=[x/10. for x in range(-20,20)])

expr = toolbox.individual()
pop = toolbox.population(n=5)
for ind in pop:
    ind.specie(1)

print 'contando especies: ',count_species(pop)
pop+=toolbox.population(n=5)
species(pop, 0.15)
print 'obteniendo especies despues de...'
for ind in pop:
    print ind.get_specie()
