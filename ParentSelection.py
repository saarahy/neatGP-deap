from deap import gp

class p_selection():
    def p_selection(self, population):
        q=list()
        for ind in population:
            ind.descendent(num_desc(ind, avg(population)))
        q=population
        for ind in q:
            print 'eliminar individuos'
    #ordenar individuos basados en penalizacion
    def num_desc(self, ind, avg):
        print 'num de descendientes de cada individuo'

    def avg(self, population):
        print 'promedio de fitness de la poblacion'