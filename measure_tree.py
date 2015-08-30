from __future__ import division
from deap import base, creator, gp, tools
def distance(ind1, ind2):
#def distance(Ti, Tj):
#ind=[ind for ind in population]
    b=0.5
    Nij=len(ind1)+len(ind2)
    Dij=(ind1.height+1)+(ind2.height+1)
    common_tree=compare_tree(ind1,ind2)
    nsij=common_tree[0] #2
    dsij=common_tree[1] #1
    d1=b*((Nij-(2*nsij))/(Nij-2))
    d2=(1-b)*((Dij-(2*dsij))/(Dij-2))
    d=d1+d2
    #out=open('dis.txt', 'a')
    #out.write('\n Nij, Dij, nsij, dsij, d1, d2, ind1, ind2 %s %s %s %s %s %s %s %s' %
    #          (Nij, Dij, nsij, dsij, d1, d2, ind1, ind2))
    #out.close()
    #ind=[ind for ind in population]
    #distance=len(ind)
    return d


def compare_tree(ind1, ind2):
    level1=level_node(ind1)
    level2=level_node(ind2)
    min_nodes=min(max(level1)[0], max(level2)[0])
    num_nodes=0
    tot_depth=0
    for i in  range(min_nodes):
        if(level1[0]==level2[0] and level1[i][0]==0):
            num_nodes=1+level1[i][2]
        elif(level1[i]==level2[i]):
            num_nodes+=level1[i][2]
        tot_depth=level1[i+1][1]
    #out=open('level.txt','a')
    #out.write('\n level1 level 2 ind1 ind2 %s %s %s %s ' %(level1, level2, ind1, ind2))
    #out.close()
    return num_nodes, tot_depth

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
    if len(expr)<2:
        level.append([edge[0][0], contador, 0])
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
