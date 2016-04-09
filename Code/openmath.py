
"""

Module contains methods for two way processing between OM files (or strings) and Python objects

"""

###############
#   imports   #
###############

import xml.etree.ElementTree as ET
Element = ET.Element
SubElement = ET.SubElement
from omparse import *
from omput import *
from os import *

######################################################
#   functions for processing OM and Python objects   #
######################################################

def ParseOMfile(fname):
    """
    converts a file containing an OM string into a python object

    """
    if not path.isfile(fname):
        return ProgramErrorObj("file_not_found",fname)
    tree = ET.parse(fname)
    root = tree.getroot()
    omobj = ParseOMroot(root)
    return omobj


def ParseOMstring(omstring):
    """
    converts an OM string to a python object

    """
    root = ET.fromstring(omstring)
    omobj = ParseOMroot(root)
    return omobj


def process(fileIN, fileOUT):
    """
    processes the openmath contents of fileIN
    >> converts result to openmath format
    >> writes the result to fileOUT

    returns the result packaged into a PythonOM object,
    which contains the result in both formats

    """
    # # processes the contents of fileIN, gets result as omobj
    # gets result as python object
    pythObj= ParseOMfile(fileIN)
    if isinstance(pythObj,ProgramErrorObj):
        return pythObj
    # converts result to string in openmath format
    omstring = OMprettystring(OMobject(pythObj),0)
    writeToFile(fileOUT, omstring)

    # packages result into a PythonOM object
    return PythonOM(pythObj,omstring)

##############################
#   functions for printing   #
##############################

def OMprint( x ):
    """
    prints a python object in OM format using pretty printing

    """
    print( OMprettystring( OMobject( x ), 0 ) )


def OMstring( x ):
    """
    returns a python object as a non-indented OM string

    """
    return ET.tostring( OMobject( x ) )


def OMprettystring( obj, level ):
    """
    returns an OM string with appropriate indentation

    """
    string = '\n' + level * 4 * ' ' + '<' + obj.tag
    for value,key in obj.attrib.items():
        string += ' {}=\'{}\''.format(value,key)
    if obj.text:
        string += '>'
        string += str(obj.text)
        string += '</' + obj.tag + '>'
    elif obj:
        string += '>'
        for child in obj:
            string += OMprettystring( child, level+1 )
        string += '\n' + level * 4 * ' ' + '</' + obj.tag + '>'
    else:
        string += " />"
    return string


#################
#   auxiliary   #
#################

class PythonOM:
    def __init__(self,pyth,omstring):
        self.python= pyth
        self.openmath= omstring


def writeToFile(filename, str):
    """
    writes string to file filename

    """
    f = open(filename, 'w')
    f.write(str)
