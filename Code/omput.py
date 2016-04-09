"""
Module contains methods for converting python objects into OM strings

"""

###############
#   imports   #
###############

import xml.etree.ElementTree as ET
Element = ET.Element
SubElement = ET.SubElement

from omparse import Matrix, MatrixRow, OMErrorObj
import fractions

##############################################
#   Python object to OM element converters   #
##############################################

##############################
#   OpenMath integer (OMI)   #
##############################

def OMInt( x ):
    omelt = Element("OMI")
    omelt.text = str(x)
    return omelt

###########################
#   OpenMath float (OMF)  #
###########################

def OMFloat (x):
    omelt = Element("OMF")
    value = str(x)
    omelt.attrib = {'dec':value }
    return omelt

#############################################
#   OpenMath rational number symbol (OMS)   #
#############################################

def OMRational(x) :
    omelt = Element ("OMA")
    oms=  Element ("OMS")
    oms.attrib={'cd':'nums1', 'name':'rational'}
    omelt.insert(1,oms)
    omi = OMInt(x.numerator)
    omelt.insert(2,omi)
    omi = OMInt(x.denominator)
    omelt.insert(3,omi)
    return omelt

###############################
#   OpenMath string (OMSTR)   #
###############################

def OMStr (x):
    omelt = Element("OMSTR")
    omelt.text = str(x)
    return omelt

############################################
#   OpenMath complex number symbol (OMS)   #
############################################

def OMComplex (x):
    omelt = Element ("OMA")
    oms = Element ("OMS")
    oms.attrib = {'cd': 'complex1', 'name' : 'complex_cartesian'}
    omelt.insert(1,oms)
    real= int(x.real) if ((x.real).is_integer()) else x.real
    imag= int(x.imag) if ((x.imag).is_integer()) else x.imag
    omelt.insert(2,OMelement(real))
    omelt.insert(3,OMelement(imag))
    return omelt

########################################
#   OpenMath matrix row symbol (OMS)   #
########################################

def OMMatrixRow(x):
    omelt = Element("OMA")
    oms = Element("OMS")
    oms.attrib = {'cd' : 'linalg2', 'name' : 'matrixrow'}
    omelt.insert(1, oms)
    i = 2
    for cell in x.cells:
        omcell = OMelement(cell)
        omelt.insert(i, omcell)
    return omelt

####################################
#   OpenMath matrix symbol (OMS)   #
####################################

def OMMatrix(x):
    omelt = Element("OMA")
    oms = Element("OMS")
    oms.attrib = {'cd' : 'linalg2', 'name' : 'matrix'}
    omelt.insert(1, oms)
    i = 2
    for row in x.rows:
        omrow = OMMatrixRow(row)
        omelt.insert(i,omrow)
        i += 1
    return omelt

###########################################
#   OpenMath boolean value symbol (OMS)   #
###########################################

def OMBool(x):
    oms = Element("OMS")
    value = 'true' if x else 'false'
    oms.attrib = {'cd' : 'logic1', 'name' : value}
    return oms

############################
#   Openmath error (OME)   #
############################

def OMError(x) :
    omelt = Element("OME")
    oms = Element("OMS")
    # x is of type OMErrorObject
    # its name attribute contains the name of the OM error
    oms.attrib = {'cd': 'error', 'name' : x.name}
    omelt.insert(1, oms)
    omelt.insert(2, x.context)
    return omelt

#####################
#   Openmath list   #
#####################

def OMList(x):
    omelt = Element("OMA")
    oms = Element("OMS")
    oms.attrib = { 'cd' : 'list1', 'name' : 'list' }
    omelt.insert(1, oms)
    n = 1
    for t in x:
        n = n + 1
        omelt.insert(n, OMelement(t))
    return omelt

#################
#   OMelement   #
#################

def OMelement(x):
    """
    dispatches OpenMath encoding method dependently on the type of x

    """
    if isinstance(x, Matrix):
        return OMMatrix(x)
    if isinstance(x, OMErrorObj):
        return OMError(x)
    t = type (x)
    if t == int:
        return OMInt(x)
    elif t == list:
        return OMList(x)
    elif t == str:
        return OMStr(x)
    elif t == float:
        return OMFloat(x)
    elif t == complex:
        return OMComplex(x)
    elif t == bool:
        return OMBool(x)
    elif t == fractions.Fraction:
        return OMRational(x)
    else:
        return ProgramErrorObj("unsupported_python_object", x)

################
#   OMobject   #
################

def OMobject(x):
    """
    wraps OpenMath encoding for x into OpenMath object

    """
    omobj = Element("OMOBJ")
    omobj.insert(1, OMelement(x))
    return omobj
