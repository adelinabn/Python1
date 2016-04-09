
"""

Module contains methods for converting OM strings into Python objects

"""

###############
#   imports   #
###############

from fractions import Fraction
import arith_func
from arith_func import *

###############
#   classes   #
###############

class Matrix:
    """
    returns a matrix given the list of its rows

    """
    def __init__ (self, ls):
        self.rows = ls
    def __eq__ (self,other):
        if isinstance(other,self.__class__):
            return self.rows == other.rows


class MatrixRow:
    """
    returns a matrix row given the list of the values in that row

    """
    def __init__(self,ls):
        self.cells = ls
    def __eq__ (self,other):
        if isinstance(other,self.__class__):
            return self.cells == other.cells


class OMErrorObj:
    """
    returns an openmtah error object with name detailing the type of error
    and the context in which the error occured (e.g. a node)

    """
    def __init__(self,errortype,context):
        self.name = errortype
        self.context = context
    def __eq__ (self,other):
        if isinstance(other,self.__class__):
            o = other.name == self.name
            oc = other.context
            sc = self.context
            o= o and oc.attrib== sc.attrib
            return o

class ProgramErrorObj(Exception):
    """
    returns an object to represent an error that
    has prevented the program from performing
    the conversion between openmath and Python
    (and vice-versa)

    """
    def __init__(self,errortype,context):
        self.name = errortype
        self.context = context  # the context in which the error
                                # has occured, e.g. a tag that
                                # was not found



#######################################
#   OMS to Python object converters   #
#######################################

#####################
#   miscellaneous   #
#####################

# list1.list
def oms_list1_list(list):
    return list

# complex1.complex_cartesian
def oms_complex1_cartesian(list):
    return complex(list[0],list[1])

################
#   linalg2    #
################

# linalg2.matrix
def oms_linalg2_matrix(ls):
    m = Matrix(ls)
    return m

# linalg2.matrixrRow
def oms_linalg2_matrixRow(ls):
    s= set(ls)
    mr = MatrixRow(s)
    return mr

##############
#   nums1    #
##############

# nums1.infinity
def oms_nums1_infinity():
    return float('inf')

# nums1.rational
def oms_nums1_rational(list):
    return Fraction(int(list[0]) , int(list[1]))

#################
#   integer1    #
#################

# integer1_factorial
def oms_integer1_factorial(ls):
    return factorial(ls[0])

# interval1.interval
def oms_interval1_interval(ls):
    return list(range(ls[0],ls[1]+1))

##################
#     arith1     #
#   (complete)   #
##################

# arith1.plus
def oms_arith1_plus (ls):
    return plus (ls[0],ls[1])

# arith1.minus
def oms_arith1_minus (ls):
    return minus (ls[0],ls[1])

# arith1.times
def oms_arith1_times (ls):
    return times(ls[0],ls[1])

# arith1.divide
def oms_arith1_divide (ls):
    return divide (ls[0],ls[1])

# arith1.abs
def oms_arith1_abs(ls):
    return abs(ls[0])

# arith1.power
def oms_arith1_power(ls):
    return pow(ls[0], ls[1])

# arith1.root
def oms_arith1_root(ls):
     return root(ls[0], ls[1])

# arith1.unary_minus
def oms_arith1_unary_minus(ls):
    return unary_minus(ls[0])

# arith1.gcd
def oms_arith1_gcd(ls):
    return gcd(ls[0],ls[1])

# arith1.lcm
def oms_arith1_lcm(ls):
    return  lcm(ls[0], ls[1])

# arith1.sum
def oms_arith1_sum (ls):
    return ar_sum(ls[1],ls[0])

# arith1.product
def oms_arith1_product(ls):
    return ar_product(ls[1],ls[0])

#############
#   fns1    #
#############

def oms_fns1_lambda(children):
    """
    returns a lambda function (may be nested)
    equivalent to the OMS representation

    """
    env={}
    variables = children[0] # list of children of ombvar
    body = children[1]
    return eval(variables,body,env)


#####################################
#   Openmath content dictionaries   #
#####################################

omdicts = {}
omdicts['list1'] = {}
omdicts['logic1'] = {}
omdicts['nums1']={}
omdicts['complex1']={}
omdicts['interval1'] ={}
omdicts['linalg2'] ={}
omdicts['arith1']={}
omdicts['integer1']={}
omdicts['fns1']={}
omdicts['arith2']={}

omdicts['list1']['list'] = oms_list1_list
omdicts['logic1']['true'] = True
omdicts['logic1']['false'] = False
omdicts['nums1']['rational']=oms_nums1_rational
omdicts['nums1']['infinity']=oms_nums1_infinity
omdicts['complex1']['complex_cartesian']=oms_complex1_cartesian
omdicts['interval1']['integer_interval']=oms_interval1_interval
omdicts['linalg2']['matrixrow'] = oms_linalg2_matrixRow
omdicts['linalg2']['matrix'] = oms_linalg2_matrix
omdicts['arith1']['plus'] = oms_arith1_plus
omdicts['arith1']['minus'] = oms_arith1_minus
omdicts['arith1']['times'] = oms_arith1_times
omdicts['arith1']['divide'] = oms_arith1_divide
omdicts['arith1']['abs'] = oms_arith1_abs
omdicts['arith1']['power'] = oms_arith1_power
omdicts['arith1']['root'] = oms_arith1_root
omdicts['arith1']['lcm'] = oms_arith1_root
omdicts['arith1']['unary_minus'] = oms_arith1_unary_minus
omdicts['arith1']['gcd'] = oms_arith1_gcd
omdicts['arith1']['lcm'] = oms_arith1_lcm
omdicts['arith1']['sum'] = oms_arith1_sum
omdicts['arith1']['product'] = oms_arith1_product
omdicts['integer1']['factorial'] = oms_integer1_factorial
omdicts['fns1']['lambda'] = oms_fns1_lambda
omdicts['arith2']['inverse'] = OMErrorObj("not implemented",None)

########################
#   Openmath parsers   #
########################


def ParseOMI(node):
    """
    returns the integer value represented by OMI node

    """
    return int(node.text)

def ParseOMF(node):
    """
    returns the float value represented by OMF node

    """
    value = node.get('dec')
    return float(value)


def ParseOMSTR(node):
    """
    return the string represented by OMSTR node

    """
    return str(node.text)



def ParseOMS(node):
    """
    returns function associated with the symbol represented by OMS
    if function not found or not implemented returns errUnexpectedSymbol object

    """
    # returns a function or an object
    cd_name = node.get('cd')
    if not cd_name in omdicts:
        return OMErrorObj("unsupported_CD", node)
    f_name = node.get('name')
    if not f_name in omdicts[cd_name]:
        # symbol not found in the content dictionary
        return OMErrorObj("unexpected_symbol", node)
    # if symbol found, get the obj with that name in the content dictionary
    func = omdicts[cd_name][f_name]
    if isinstance(func, OMErrorObj):
        # if obj is not a function, symbol was not implemented correctly
        return OMErrorObj("unsupported_symbol", node)
    # if it is a function, return it
    return func


def ParseOMA(node):
    """
    retrieves the functions associated with the OMS element
    applies it to the following elements
    or returns and Error Object

    """
    oms = node[0]
    f = ParseOMelement(oms)
    # check if parsing the symbol doesn't return an error object
    if isinstance(f, OMErrorObj):
        return f
    # if not error object, then it must have returned a function
    # parse the rest of the elements
    elts = []
    for child in node[1:]:
        elts.append( ParseOMelement(child) )
    # apply function to the rest of the OM elements
    return f(elts)


def ParseOMBIND(node):
    """
    returns a (possibly nested) lambda function described inside the OMBIND element
    a nested lambda function will be called with f(arg1)(arg2)(arg3)...
    if such a function contains only one variable, it may be flattened using:
    arith_func.flatten()

    """
    oms = node[0]
    children = node[1:]
    # passing the lambda OMBVAR and function body
    # to function that evaluates a lambda OM object
    f = ParseOMS(oms)
    if isinstance(f, OMErrorObj):
        return f
    return f(children)


def ParseOME(node):
    """
    returns an OMErrorObj associated with the OME element

    """
    # the second child is the original erroneous OMS node
    # parsing it will produce an OMErrorObj, see ParseOMS
    return ParseOMS(node[1])


def ParseOMelement(obj):
    """
    applies the parser corresponding to the obj OM element

    """
    if obj.tag in ParseOMelementHandler:
        return ParseOMelementHandler[obj.tag](obj)
    else:
        return ProgramErrorObj("unknown_tag", obj.tag)


def ParseOMroot(root):
    """
    parses the root element of the OM object

    """
    if not root.tag == 'OMOBJ':
        return ProgramErrorObj("unknown_tag", root.tag)
    if len(root) > 0:
        return ParseOMelement(root[0])
    else:
        return ProgramErrorObj("nothing_to_parse", root.tag)


#################
#   auxiliary   #
#################

ParseOMelementHandler = {   'OMI'       : ParseOMI,
                            'OMS'       : ParseOMS,
                            'OMA'       : ParseOMA,
                            'OMSTR'     : ParseOMSTR,
                            'OMF'       : ParseOMF,
                            'OMBIND'    : ParseOMBIND,
                            'OME'       : ParseOME
                        }


def eval(vs,body,env):
    """
    reads variable declarations (vs) and populates the variable environment (env)
    returns a function given its body (body)

    """
    if len(vs)>0: # i.e. we still have a child node inside OMBVAR - a variable
        varname = vs[0].get('name')         # extract the name of the variable
        # create a pointer for this variable -x and add it to the environment
        # continue to evaluate either other varible declarations or the function body
        vs = [] if (len(vs)==1) else vs[1:]
        return lambda x: eval(vs, body,updateEnv(varname,x,env))

    # no more variable declarations at this point, so we can start evaluating the function
    # body given the populated environment env
    return evalBody(body,env)


def evalBody(body,env):
    """
    returns the function (or part of the function) with
    a given function body description in OMS format

    """
    if body.tag== "OMA":
        # evaluate both sides of the expression
        f_name = body[0].get('name') # name of arith1 function
        f= arithmetic_func[f_name]   # get the arithmetic function
                                     # corresponding to OMS element
        arg1 = evalBody (body[1],env)
        if f.__name__ in singleArg:  # if f requires only one arg
            return f(arg1)
        arg2 = evalBody (body[2], env)
        return f(arg1,arg2)

    if body.tag =="OMV":
         # return pointer associated with that variable name
        name = body.get('name')
        return env[name]
    # parse any other element like int, float etc.
    return ParseOMelement(body)


def updateEnv(name, var, env):
    """
    adds a new name - pointer relation to the variable environment (dictionary)
    returns the updated environment

    """
    env[name] = var
    return env
