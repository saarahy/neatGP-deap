from deap import base, creator, gp, tools
import  operator
from crosspoints import *

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.renameArguments(ARG0='x')

creator.create("Individual", gp.PrimitiveTree)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)

expr = toolbox.individual()
expr2 = toolbox.individual()
nodes, edges, labels = gp.graph(expr)

print 'expr:',expr
print 'expr2:',expr2

cxp=crosspoints(expr,expr2)
print cxp
#print distance(expr,expr2)

print neatcx(expr, expr2)
species(pop, 0.15)