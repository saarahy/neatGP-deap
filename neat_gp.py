from deap import gp
class neat(gp.PrimitiveTree):
    #propiedades de la especiacion
    #cambio para neat
    def specie(self,sp):
        self.tspecie=sp

    def get_specie(self):
        return self.tspecie