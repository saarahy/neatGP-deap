from __future__ import division
from deap import base, creator, gp, tools

#determina la distancia entre un individuo y otro
#ecuacion 2
#regresa un numero
def distance(ind1, ind2):
#def distance(Ti, Tj):
#ind=[ind for ind in population]
    b=0.5
    Nij=len(ind1)+len(ind2) #34
    Dij=(ind1.height+1)+(ind2.height+1) #6
    common_tree=compare_tree(ind1,ind2) #3,2
    nsij=common_tree[0] #3
    dsij=common_tree[1] #2
    d1=b*((Nij-(2*nsij))/(Nij-2))
    d2=(1-b)*((Dij-(2*dsij))/(Dij-2))
    d=d1+d2
    return d

#compara el numero de nodos y la profundidad
# que tienen dos individuos
#regresa una tupa con (num_nodes, tot_depth)
def compare_tree(tree1, tree2):
    nodo=0
    lista_nivel=list()
    expr1=level_node(tree1)
    expr2=level_node(tree2)

    for ind1 in expr1:
        for ind2 in expr2:
            if ind1==ind2 and ind1[0]==0:
                nodo+=1
                lista_nivel.append(ind1[1])
                break
            elif tot_grpo(expr1, ind1[1])==2 and tot_grpo(expr2, ind1[1])==2 and ind1[1] not in lista_nivel:
                nodo+=2
                lista_nivel.append(ind1[1])
                break
            elif tot_grpo(expr1, ind1[1])<tot_grpo(expr2, ind1[1]) and ind1[1] not in lista_nivel:
                total=tot_grpo(expr1,ind1[1])
                nodo+=total
                if total>0:
                    lista_nivel.append(ind1[1])
                break
            elif tot_grpo(expr1, ind1[1])>tot_grpo(expr2, ind1[1]) and ind1[1] not in lista_nivel:
                total=tot_grpo(expr2,ind1[1])
                nodo+=total
                if total>0:
                    lista_nivel.append(ind1[1])
                break
            elif tot_grpo(expr1, ind1[1])==tot_grpo(expr2, ind1[1]) and ind1[1] not in lista_nivel:
                total=tot_grpo(expr2,ind1[1])
                nodo+=total
                if total>0:
                    lista_nivel.append(ind1[1])
                break
            elif ind1[1] in lista_nivel:
                break
    return nodo, max(lista_nivel)

#revisa cada uno de los nodos indicando su posicion
#en el nivel, su aridad y su numero de nodo
#regresa una lista [num_nodo, nivel, aridad]
def level_node(expr):
    nodes, edges, labels = gp.graph(expr)
    #outfile = open('edges.txt', 'a')
    edge=sorted(edges)
    #outfile.write('\n edges expre %s %s ' % (edge,expr))
    #outfile.close()
    contador=1
    nod=0
    level=list()
    restart=True
    #numnodo #numnivel #aridad
    if len(expr)<2:
        level.append([0, contador, 0])
    else:
        level.append([edge[0][0], contador, expr[0].arity])
        for i in range(max(nodes)):
            restart=True
            contador=1
            nod=i+1
            while restart:
                restart=False
                for j in range(max(nodes)):
                    if edge[j][1]==nod:
                        contador+=1
                        nod=edge[j][0]
                    if(nod>0 and contador>1):
                        restart=True
            level.append([i+1, contador, expr[i+1].arity])
    return level

def tot_grpo(exp,nivel):
    total=0
    for i in exp:
        if i[1]==nivel:
            total+=1
    return total