def convrt(strg):
        strg = strg.replace(" ","")
        str2=strg.replace('(',',')
        str2=str2.replace(')',',')
        text=str2.split(',')
        str_list = filter(None, text)
        return str_list

def convrt_token(strg):
        strg = strg.replace(" ","")
        str2=strg.replace('(',',')
        str2=str2.replace(')',',')
        text=str2.split(',')
        str_list = filter(None, text)
        return str_list

def add_subt_cf(strg, args):
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
    if len(args)>1:
        for id in args:
            if id in lin_tree:
                num_x=lin_tree.count(id)
                for numx in range(num_x):
                    idx=lin_tree.index(id)
                    t=lin_tree[idx]
                    ax=t[0]
                    an=t[1]
                    lin_tree[idx]='%s[%s]'%(ax,an)
    return lin_tree

def add_subt(strg, ind):
    params=ind.get_params()
    st=strg
    str2add=convrt_token(st)
    str_linear=['add', str(params[0]), 'mul', str(params[1])]
    lin_tree=[]
    for n in range(2,len(str2add)+2):
        cad='mul(%s)' % params[n]
        # print params
        # print str2add
        cad=convrt_token(cad)
        cad.append(str2add[n-2])
        lin_tree= lin_tree + cad
    lin_tree = str_linear + lin_tree
    return lin_tree