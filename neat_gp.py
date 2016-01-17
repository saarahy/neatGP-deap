class neat:
    #propiedades de la especiacion
    #cambio para neat
    def specie(self,sp):
        self.tspecie=sp

    def get_specie(self):
        return self.tspecie

    def fitness_sharing(self, avg):
        self.fitness_h=avg

    def get_fsharing(self):
        return self.fitness_h

    def descendents(self, des):
        self.descendent=des

    def get_descendents(self):
        return self.descendent

    def penalty(self, p):
        self.penalizado=p

    def num_specie(self,ns):
        self.nspecie=ns

    def get_numspecie(self):
        return self.nspecie

    def LS_probability(self, ps):
        self.LS_prob=ps

    def get_LS_prob(self):
        return self.LS_prob

    def params_set(self, params):
        self.params=params

    def get_params(self):
        return self.params

    def bestspecie_set(self, value):
        self.best_ind=value

    def bestspecie_get(self):
        return self.best_ind

    def LS_applied_set(self, value):
        self.ls_ind=value

    def LS_applied_get(self):
        return self.ls_ind

    def LS_fitness_set(self,value):
        self.ls_fitness=value

    def LS_fitness_get(self):
        return self.ls_fitness

class pop_param:
    def save_ind(self):
        return True