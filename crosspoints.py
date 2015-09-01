import random
import copy
from measure_tree import *

def neatcx(ind1, ind2):
    e1,e2=ext_node(ind1,ind2)
    l1,l2, p1, p2=int_node(ind1,ind2)

    for i in p1:
        if random.random()<0.5:
            print 'cambio nodo'
            l=random.choice(l2)
            #p=random.choice(p2)
            ind1[i]=l
            break
    print 'ind mod node:',ind1
    for i in e1:
        if random.random()<0.5:
            print 'cambio'
            e=random.choice(e2)
            #print ind1,e
            slice1=ind1.searchSubtree(i)
            slice2=ind2.searchSubtree(e)
            ind1[slice1], ind2[slice2]=ind2[slice2], ind1[slice1]
            break
    return  ind1

def int_node(ind1, ind2):
    cont1=0
    cont2=0
    label1=list()
    label2=list()
    pos1=list()
    pos2=list()
    maxim=max(len(ind1), len(ind2))
    #print 'maxim',maxim
    while (cont1<maxim) and (cont2<maxim):
        #print 'c1',cont1,'c2',cont2
        if ind1[cont1].arity==ind2[cont2].arity and ind1[cont1].arity>0:
            label1.append(ind1[cont1])
            label2.append(ind2[cont2])
            pos1.append(cont1)
            pos2.append(cont2)
            cont1+=1
            cont2+=1
        elif ind1[cont1].arity==ind2[cont2].arity and ind1[cont1].arity==0:
            cont1+=1
            cont2+=1
        else:
            if ind1[cont1].arity>0:
                copia=copy.deepcopy(ind1)
                slice1=copia.searchSubtree(cont1)
                copia[1:]=copia[slice1]
                long=len(copia)-1
                cont1+=long
                cont2+=1
            elif ind2[cont2].arity>0:
                copia=copy.deepcopy(ind2)
                slice1=copia.searchSubtree(cont2)
                copia[1:]=copia[slice1]
                long=len(copia)-1
                cont2+=long
                cont1+=1
    return label1,label2, pos1, pos2

def ext_node(ind1, ind2):
    cont1=0
    cont2=0
    edg1=list()
    edg2=list()
    maxim=max(len(ind1), len(ind2))
    #print 'maxim',maxim
    while (cont1<maxim) and (cont2<maxim):
        #print 'c1',cont1,'c2',cont2
        if ind1[cont1].arity==ind2[cont2].arity and ind1[cont1].arity>0:
            cont1+=1
            cont2+=1
        elif ind1[cont1].arity==ind2[cont2].arity and ind1[cont1].arity==0:
            edg1.append(cont1)
            edg2.append(cont2)
            cont1+=1
            cont2+=1
        else:
            edg1.append(cont1)
            edg2.append(cont2)
            if ind1[cont1].arity>0:
                copia=copy.deepcopy(ind1)
                slice1=copia.searchSubtree(cont1)
                copia[1:]=copia[slice1]
                long=len(copia)-1
                cont1+=long
                cont2+=1
            elif ind2[cont2].arity>0:
                copia=copy.deepcopy(ind2)
                slice1=copia.searchSubtree(cont2)
                copia[1:]=copia[slice1]
                long=len(copia)-1
                cont2+=long
                cont1+=1
    return edg1,edg2

def crosspoints(tree1, tree2):
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

def grupo(exp,nivel):
    grupo=list()
    for i in exp:
        if i[1]==nivel:
            grupo.append(i)
    return grupo

def tot_grpo(exp,nivel):
    total=0
    for i in exp:
        if i[1]==nivel:
            total+=1
    return total
