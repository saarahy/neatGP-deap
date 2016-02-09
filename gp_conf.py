import copy
import random
import re
import sys
import warnings
import numpy as np
import operator
from collections import defaultdict, deque
from functools import partial, wraps
from inspect import isclass
from operator import eq, lt
from neat_gp import *
from deap import gp
######################################
# GP Data structure                  #
######################################

# Define the name of type for any types.
__type__ = object


class PrimitiveTree(gp.PrimitiveTree, neat):
    """Tree spefically formated for optimization of genetic
    programming operations. The tree is represented with a
    list where the nodes are appended in a depth-first order.
    The nodes appended to the tree are required to
    have an attribute *arity* which defines the arity of the
    primitive. An arity of 0 is expected from terminals nodes.
    """
    def __init__(self, content):
        list.__init__(self, content)
        self.tspecie = None
        self.descendent = None
        self.fitness_h = None
        self.nspecie = None
        self.params = None
        self.best_ind = None

    def __deepcopy__(self, memo):
        new = self.__class__(self)
        new.__dict__.update(copy.deepcopy(self.__dict__, memo))
        return new

    def __setitem__(self, key, val):
        # Check for most common errors
        # Does NOT check for STGP constraints
        if isinstance(key, slice):
            if key.start >= len(self):
                raise IndexError("Invalid slice object (try to assign a %s"
                    " in a tree of size %d). Even if this is allowed by the"
                    " list object slice setter, this should not be done in"
                    " the PrimitiveTree context, as this may lead to an"
                    " unpredictable behavior for searchSubtree or evaluate."
                     % (key, len(self)))
            total = val[0].arity
            for node in val[1:]:
                total += node.arity - 1
            if total != 0:
                raise ValueError("Invalid slice assignation : insertion of"
                    " an incomplete subtree is not allowed in PrimitiveTree."
                    " A tree is defined as incomplete when some nodes cannot"
                    " be mapped to any position in the tree, considering the"
                    " primitives' arity. For instance, the tree [sub, 4, 5,"
                    " 6] is incomplete if the arity of sub is 2, because it"
                    " would produce an orphan node (the 6).")
        elif val.arity != self[key].arity:
            raise ValueError("Invalid node replacement with a node of a"
                             " different arity.")
        list.__setitem__(self, key, val)

    def __str__(self):
        """Return the expression in a human readable string.
        """
        string = ""
        stack = []
        for node in self:
            stack.append((node, []))
            while len(stack[-1][1]) == stack[-1][0].arity:
                prim, args = stack.pop()
                string = prim.format(*args)
                if len(stack) == 0:
                    break   # If stack is empty, all nodes should have been seen
                stack[-1][1].append(string)

        return string

    @classmethod
    def from_string(cls, string, pset):
        """Try to convert a string expression into a PrimitiveTree given a
        PrimitiveSet *pset*. The primitive set needs to contain every primitive
        present in the expression.

        :param string: String representation of a Python expression.
        :param pset: Primitive set from which primitives are selected.
        :returns: PrimitiveTree populated with the deserialized primitives.
        """
        tokens = re.split("[ \t\n\r\f\v(),]", string)
        expr = []
        ret_types = deque()
        for token in tokens:
            if token == '':
                continue
            if len(ret_types) != 0:
                type_ = ret_types.popleft()
            else:
                type_ = None

            if token in pset.mapping:
                primitive = pset.mapping[token]

                if len(ret_types) != 0 and primitive.ret != type_:
                    raise TypeError("Primitive {} return type {} does not "
                                    "match the expected one: {}."
                                    .format(primitive, primitive.ret, type_))

                expr.append(primitive)
                if isinstance(primitive, gp.Primitive):
                    ret_types.extendleft(reversed(primitive.args))
            else:
                try:
                    token = eval(token)
                except NameError:
                    raise TypeError("Unable to evaluate terminal: {}.".format(token))

                if type_ is None:
                    type_ = type(token)

                if type(token) != type_:
                    raise TypeError("Terminal {} type {} does not "
                                    "match the expected one: {}."
                                    .format(token, type(token), type_))

                expr.append(gp.Terminal(token, False, type_))
        return cls(expr)

    @property
    def height(self):
        """Return the height of the tree, or the depth of the
        deepest node.
        """
        stack = [0]
        max_depth = 0
        for elem in self:
            depth = stack.pop()
            max_depth = max(max_depth, depth)
            stack.extend([depth+1] * elem.arity)
        return max_depth

    # @property
    # def params(self):
    #     l=len(self)+4
    #     p=np.ones(l)
    #     return p


    @property
    def root(self):
        """Root of the tree, the element 0 of the list.
        """
        return self[0]

    def searchSubtree(self, begin):
        """Return a slice object that corresponds to the
        range of values that defines the subtree which has the
        element with index *begin* as its root.
        """
        end = begin + 1
        total = self[begin].arity
        while total > 0:
            total += self[end].arity - 1
            end += 1
        return slice(begin, end)


def cxOnePoint(ind1, ind2):
    """Randomly select in each individual and exchange each subtree with the
    point as root between each individual.

    :param ind1: First tree participating in the crossover.
    :param ind2: Second tree participating in the crossover.
    :returns: A tuple of two trees.
    """
    if len(ind1) < 2 or len(ind2) < 2:
        # No crossover on single node tree
        return ind1, ind2

    # List all available primitive types in each individual
    types1 = defaultdict(list)
    types2 = defaultdict(list)
    if ind1.root.ret == __type__:
        # Not STGP optimization
        types1[__type__] = xrange(1, len(ind1))
        types2[__type__] = xrange(1, len(ind2))
        common_types = [__type__]
    else:
        for idx, node in enumerate(ind1[1:], 1):
            types1[node.ret].append(idx)
        for idx, node in enumerate(ind2[1:], 1):
            types2[node.ret].append(idx)
        common_types = set(types1.keys()).intersection(set(types2.keys()))

    if len(common_types) > 0:
        type_ = random.choice(list(common_types))
        index1 = random.choice(types1[type_])
        index2 = random.choice(types2[type_])
        slice1 = ind1.searchSubtree(index1)
        slice2 = ind2.searchSubtree(index2)

        ind1[slice1], ind2[slice2] = ind2[slice2], ind1[slice1]

    return ind1, ind2


def mutUniform(individual, expr, pset):
    """Randomly select a point in the tree *individual*, then replace the
    subtree at that point as a root by the expression generated using method
    :func:`expr`.

    :param individual: The tree to be mutated.
    :param expr: A function object that can generate an expression when
                 called.
    :returns: A tuple of one tree.
    """
    index = random.randrange(len(individual))
    slice_ = individual.searchSubtree(index)
    type_ = individual[index].ret
    individual[slice_] = expr(pset=pset, type_=type_)
    return individual,
