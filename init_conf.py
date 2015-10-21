def initRepeat(container, func, n):
    """Call the function *container* with a generator function corresponding
    to the calling *n* times the function *func*.
    
    :param container: The type to put in the data from func.
    :param func: The function that will be called n times to fill the
                 container.
    :param n: The number of times to repeat func.
    :returns: An instance of the container filled with data from func.
    
    This helper function can can be used in conjunction with a Toolbox 
    to register a generator of filled containers, as individuals or 
    population.
    
        >>> initRepeat(list, random.random, 2) # doctest: +ELLIPSIS, 
        ...                                    # doctest: +NORMALIZE_WHITESPACE
        [0.4761..., 0.6302...]

    See the :ref:`list-of-floats` and :ref:`population` tutorials for more examples.
    """
    if container==list:
        pop=[]
        for x in xrange(n):
            ind=func()
            if ind in pop:
                n1=0
                while n1<20:
                    ind=func()
                    if ind in pop:
                        n1+=1
                    else:
                        pop.append(ind)
                        break
                if n1>=20:
                    pop.append(ind)
            else:
                pop.append(ind)
        container=pop
        return container
    else:
        return container(func() for _ in xrange(n))
