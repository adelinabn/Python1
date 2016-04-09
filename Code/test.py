
"""

Module contains tests that involve processing OM files
and displaying (+saving) the result in OM format

input files  :             tst directory
output files :             tst_out directory

The result of processing each file from tst directory
( both as a Python object and an OM object )
is compared to the expected one, if it has been provided,
and the outcome of the test is displayed

"""

###############
#   imports   #
###############

import openmath
from openmath import *
import os


######################
#   test functions   #
######################

def test_from_dir(dir_IN, dir_OUT):
    """
    >> Processes all files from dir_IN writing the results
       to corresponding files in dir_OUT
    >> Performs a double conversion of the result :
             pythObj -> OMobj -> pythObj
       and compares it to the original one
    >> Prints outcome of the test for each file

    """
    if not (os.path.isdir(dir_IN) and os.path.isdir(dir_OUT)):
        print ("Could not find test input directory or test output directory")
        return
    counter=0    # test number index
    lf=[]        # list of files that did not pass the test
    # for all files in the input directory
    for f in os.listdir(dir_IN):
        counter+=1
        print("\n\n========================================================")
        print ("\nTEST\t", counter)
        infile = dir_IN+"/"+f
        outfile = dir_OUT+"/" +f
        result = process(infile,outfile)
        # if file was not successfully processed
        if not is_valid_result(result,f):
            lf.append(f)
        else:
            passed = False
            # if performing a double conversion returns the same object
            if result.python == ParseOMstring(OMstring(result.python)):
                passed = True
            # output appropriate message
            if passed == True:
                print ("FILE:\t",f,"\t: PASSED")
            else:
                print ("FILE:\t",f,"\t: FAILED")
                lf.append(f)
            print("RESULT:")
            print("--------------------------------------------------------")
            print(result.openmath)

    # print the general outcome of the tests
    print("--------------------------------------------------------")
    if len(lf) == 0: # all tests have passed
        print ("\nAll tests have passed.")
    else:
        print ("\nThe following files have not passed the test:\n")
        for x in lf:
            print(x)


def is_valid_result(result,filename):
    """
    returns false if processing the file filename has resulted
    in a program error - most likely a parse error
    returns true if the file was successfully processed

    """
    if isinstance(result,ProgramErrorObj):
            print ("FILE:\t",filename,"\t: FAILED")
            print("ERROR TYPE:\t",result.name)
            print("ERROR CONTEXT:\t",result.context)
            return False
    return True


def main():
    """
    sets up the directories
    calls the test method

    """
    currentDir = os.getcwd()
    tstin = currentDir + "/tst"
    tst_out = tstin + "_out"
    test_from_dir(tstin, tst_out)


###################
#  start testing  #
###################

if __name__ == '__main__':
    main()
