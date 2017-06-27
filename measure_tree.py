from __future__ import division
from deap import base, creator, gp, tools


def distance(ind1, ind2, beta):
    """
    This method determine the distance between two individuals
    Equation (2) of Leonardo Trujillo et al. neat Genetic Programming. Inf. Sci. 333, C (March 2016), 21-43.

    :param ind1: First Individual
    :param ind2: Second Individual
    :param version: This indicate the form of comparision between two individuals.
    :return: A number indicating the distance
    """

    b = beta
    Nij = len(ind1) + len(ind2)
    Dij = (ind1.height + 1) + (ind2.height + 1)

    common_tree = compare_tree(ind1, ind2)
    nsij = common_tree[0]
    dsij = common_tree[1]

    d1 = b * ((Nij - (2 * nsij)) / (Nij - 2))
    d2 = (1 - b) * ((Dij - (2 * dsij)) / (Dij - 2))

    d = d1 + d2
    return d


def compare_tree(tree1, tree2):
    """
    This method compare the number of nodes and the depth between two
    individuals.
    Binary version does not enter here

    :param tree1: First Individual
    :param tree2: Second Individual
    :param version: Original version or modify version.
    :return: a tuple with the number of nodes and the common depth
    """
    nodo = 0
    lista_nivel = list()
    list_tree1 = list()
    list_tree2 = list()
    first_node = False


    expr1 = level_node(tree1)
    expr2 = level_node(tree2)

    for ind1 in expr1:
        for ind2 in expr2:
            if ind1 == ind2 and ind1[0] == 0:
                nodo += 1
                first_node = True
                lista_nivel.append(ind1[1])
                list_tree1.append(ind1)
                list_tree2.append(ind2)
                break
            elif ind1[1] in lista_nivel:
                break
            elif ind1[1] not in lista_nivel and first_node:
                if ind1[1] - 1 in lista_nivel:
                    total = 0
                    nivel_ant = ind1[1]-1
                    for elem in range(len(list_tree1)):
                        prev_node = ind1[0]-1
                        level_= list_tree1[elem][0]
                        if list_tree1[elem][1] == nivel_ant and prev_node == list_tree1[elem][0]:
                            if list_tree2[elem][2] == list_tree1[elem][2]:
                                total = list_tree2[elem][2]
                                [list_tree2.append(x) for x in expr2 if (x[0] == list_tree2[elem][0] + 1 or x[0] == list_tree2[elem][0] + 2)]
                                [list_tree1.append(x) for x in expr1 if
                                 (x[0] == list_tree1[elem][0] + 1 or x[0] == list_tree1[elem][0] + 2)]
                    nodo += total
                    if total > 0:
                        lista_nivel.append(ind1[1])
                    break
                else:
                    break
            if not first_node:
                return 1, 1
    return nodo, max(lista_nivel)


def level_node(expr):
    """
        This method review each node in the individual
        and it indicate the level, arity and number of node.
        :param expr: Individual to take the information
        :return: a list [node_num, level, arity]
    """
    nodes, edges, labels = gp.graph(expr)
    edge = sorted(edges)
    contador = 1
    nod = 0
    level = list()
    if len(expr)<2:
        level.append([0, contador, 0])
    else:
        level.append([edge[0][0], contador, expr[0].arity])
        for i in range(max(nodes)):
            restart = True
            contador = 1
            nod = i+1
            while restart:
                restart=False
                for j in range(max(nodes)):
                    if edge[j][1] == nod:
                        contador += 1
                        nod = edge[j][0]
                    if(nod>0) and (contador>1):
                        restart = True
            level.append([i+1, contador, expr[i+1].arity])
    return level


def tot_grpo(exp,nivel):
    total=0
    for i in exp:
        if i[1]==nivel:
            total+=1
    return total


def tot_grpo_exp(exp, nivel,list_t):
    for i in exp:
        if i[1] == nivel:
            list_t.append(i)
    return list_t