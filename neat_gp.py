class neat:
    #propiedades de la especiacion
    #cambio para neat
    def specie(self,sp):
        self.tspecie=sp

    def get_specie(self):
        return self.tspecie

    def fitness_sharing(self, avg):
        self.fitness_h=avg

    def descendents(self, des):
        self.descendent=des

    def get_descendents(self):
        return self.descendent

    def penalty(self, p):
        self.penalizado=p

class pop_param:
    def save_ind(self):
        return True