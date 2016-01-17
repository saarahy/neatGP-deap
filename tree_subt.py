def convrt(strg):
        strg = strg.replace(" ","")
        str2=strg.replace('(',',')
        str2=str2.replace(')',',')
        text=str2.split(',')
        str_list = filter(None, text)
        return str_list

def add_subt_cf(strg):
    st=strg
    str2add=convrt(st)
    str_linear=['add', 'p[0]', 'mul', 'p[1]']
    lin_tree=[]
    for n in range(2,len(str2add)+2):
        cad='mul(p[%s])' % n
        cad=convrt(cad)
        cad.append(str2add[n-2])
        lin_tree= lin_tree + cad
    lin_tree = str_linear + lin_tree
    return lin_tree

def add_subt(strg, ind):
    params=ind.get_params()
    st=strg
    str2add=convrt(st)
    str_linear=['add', str(params[0]), 'mul', str(params[1])]
    lin_tree=[]
    for n in range(2,len(str2add)+2):
        cad='mul(%s)' % params[n]
        cad=convrt(cad)
        cad.append(str2add[n-2])
        lin_tree= lin_tree + cad
    lin_tree = str_linear + lin_tree
    return lin_tree