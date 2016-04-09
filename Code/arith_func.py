"""

module contains the pure mathematical functions associated with
operations from arith1 cd and factorial from integer1

"""

###############
#   imports   #
###############

from fractions import gcd
from functools import reduce
import operator
import types


####################################
#   python functions and symbols   #
#      corresponding to their      #
#     mathematical definitions     #
####################################

def plus(a, b):
    return a + b


def minus(a, b):
    return a - b


def times(a, b):
    return a * b


def divide(a, b):
    if (b == 0):
        return float('inf')
    return float(a) / float(b)


def root(number, order):
    return number ** (1 / order)


def unary_minus(a):
    return (0 - a)


def lcm(a, b):
    return (a*b // gcd (a, b))


def ar_sum(function, interval):
    """
    corresponds to the mathematical definition of sum
    applies function to all elements of interval
    returns their subsequent sum

    """
    func = flatten(function)
    return sum(map(func, interval))


def ar_product(function, interval):
    """
    corresponds to the mathematical definition of product
    applies function to all elements of interval
    returns their subsequent product

    """
    func = flatten(function)
    return product(map(func, interval))


def factorial(n):
    return product(range(1, n+1))



########################################
#   auxiliary functions & constructs   #
########################################

# list of names of the functions that only have one argument
singleArg = ['unary_minus','abs','factorial']


def flatten (func):
    """
    flattens a nested lambda function with one variable
    returns a flat function

    """
    # if function is nested, its application will yield another function
    if type(func(0)) == types.FunctionType:
        return flatten (lambda x: func(x)(x))
    # if not nested just return it
    return func


def product(iterable):
    """
    returns the product of all the values in iterable

    """
    return reduce(operator.mul, iterable, 1)


arithmetic_func = {}
arithmetic_func['plus']                 = plus
arithmetic_func['minus']                = minus
arithmetic_func['times']                = times
arithmetic_func['divide']               = divide
arithmetic_func['power']                = pow
arithmetic_func['factorial']            = factorial     # added to this file as an exception,
                                                        # since factorial is actually in integer1 cd
arithmetic_func['unary_minus']          = unary_minus
arithmetic_func['root']                 = root
arithmetic_func['gcd']                  = gcd
arithmetic_func['lcm']                  = lcm
arithmetic_func['abs']                  = abs
arithmetic_func['sum']                  = ar_sum
arithmetic_func['product']              = ar_product
