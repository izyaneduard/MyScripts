#!/usr/bin/python

###!/depot/Python-2.7.2/bin/python

import re
import random
import sys
import math

import optparse
import subprocess

"""
array size = matrixSize
random int count

"""


print  '__________Start__________\n'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main(args):



    matrixSize = int(args.matrixSize)
    size = matrixSize
    barrier = args.barrier
    x_array = []
    y_array = []

    # Generating matrix with start and finish. 
    #Ex:
    
    #. . . . .  
    #. . . . S  
    #. . . . .  
    #. . . . .  
    #. . F . .  


    array = [['.' for x in xrange(int(matrixSize))] for x in xrange(int(matrixSize))]
    array2 = [['.' for x in xrange(int(matrixSize))] for x in xrange(int(matrixSize))]


    # Checking X barriers  to be sure that they are unique.

    def check (x1,y1) :
        if ((array[y1][x1] == 'x') or (array[y1][x1] == 'S') or (array[y1][x1] == 'F')) :
            x2 =  random.randint(0, (int(matrixSize) - 1))
            y2 =  random.randint(0, (int(matrixSize) -1))
            check(x2,y2)
        else :
            array[y1][x1] = 'x'
            array2[y1][x1] = 'x'

    # Generating random X barriers according density( "barrier") .

    for f in range(int(barrier)):
        y = random.randint(0, (int(matrixSize) - 1))
        x = random.randint(0, (int(matrixSize) - 1))
        check(x,y)	


    ## Start and Finish cordinates
    # Generating random x and y coordinates for S and F    

    xs = random.randint(0, (int(matrixSize) - 1))
    ys = random.randint(0, (int(matrixSize) - 1))

    xf = random.randint(0, (int(matrixSize) - 1))
    yf = random.randint(0, (int(matrixSize) - 1))

    array[ys][xs] = 'S'
    array[yf][xf] = 'F'

    # Printing matrix view before modification

    for i in range(int(matrixSize)) :
        for j in range(int(matrixSize)) :
            
            print array[i][j],
        print "\n",

    print "--------------"

    stepx = [-1,0,1,0]
    stepy = [0,1,0,-1]

    #pre_bit = int(matrixSize)

    global fixed

    fixed = 0

    flag = [0]
    def way (xs,ys,weight,flag) :
        global fixed,f1
        for i in range(4):
            yy = int((ys + stepy[i]))
            xx = int((xs + stepx[i]))

            if ( yy < matrixSize and   xx  < matrixSize and yy >= 0 and xx >= 0) :
                bit = array[yy] [xx]
                if (bit == '.'):
                    array[yy] [xx] = weight
                    way(xx,yy,weight+1,flag)
                elif ((isinstance( bit, int ) and bit >=  weight) ):
                    array[yy] [xx] = weight
                    way(xx,yy,weight+1,flag)
                elif ((bit == 'F')) :
                    flag.append(1)
                    f = 1
                    fixed = weight
                    return
                elif ((bit == 'S')):
                    continue
        
    way(xs,ys,1,flag)



# Checking are ther any way to reach F

    def checkWay(xf,yf):
        global minx, miny , mm
        mm = 0
        xash = {}
        for i in range(4):
            yy = int((yf + stepy[i]))
            xx = int((xf + stepx[i]))
            if ( yy < matrixSize and   xx  < matrixSize and yy >= 0 and xx >= 0) :
                bit = array[yy][xx]
##                print "bit =", bit
                if isinstance( bit, int ):
#                    minx = xx
#                    miny = yy
                    xash[bit] = [yy,xx]
#                    mm = bit
        if xash.keys():
            minKey = min(xash.keys())
            miny = xash[minKey][0]
            minx = xash[minKey][1]
            mm = minKey
 ##           print "miknKey = ",[ key for key in xash]
        if mm == 0 :
            print "There is no way reach Finish !!! "

    checkWay(xf,yf)


#    for i in range(int(matrixSize)) :
#        for j in range(int(matrixSize)) :
#            
#            print array[i][j],
#        print "\n",
#
#    print "--------------"




    def shortWay (x,y,mm0) :
        flag2 = 0
        for i in range(4):
            yy = int((y + stepy[i]))
            xx = int((x + stepx[i]))

            if ( yy < matrixSize and   xx  < matrixSize and yy >= 0 and xx >= 0) :
                bit = array[yy][xx]
                if isinstance( bit, int ) and (bit ==  mm0 - 1 ):
                    flag2 = 1
                    y1 = yy
                    x1 = xx
                    
                    
        if (flag2) :
            array2[y1][x1] = '*'
            flag2 = 0
            shortWay(x1,y1,mm0-1)			

    array2[ys][xs] = 'S'
    array2[yf][xf] = 'F'

    if (mm == 0 ) :
#    if False:  #isinstance( mm, int ):
        pass
    else :

        array2[miny][minx] = '*'					
        shortWay (minx,miny,mm)
        for i in range(matrixSize) :
            for j in range(matrixSize) :
            
                if array2[i][j] == '*':
                    print bcolors.FAIL + array2[i][j] + bcolors.ENDC,

                elif array2[i][j] == 'S' or  array2[i][j] == 'F':
                    print bcolors.OKBLUE + array2[i][j] + bcolors.ENDC,

                else:    
                    print array2[i][j],

            print "\n",

def parse_args(argv):
    """ Parse the arguments.
    Parameters:
        argv - the list of arguments
    """
    parser = optparse.OptionParser(description='This script is for generate short way from start to finish in matrix',
                                    usage="usage: %prog [options] arg1 arg2", version="%prog 1.0")
    parser.add_option( '-s','--size', dest='matrixSize', help="size of matrix")
    parser.add_option( '-b','--barrier--', dest='barrier', help="density of barriers")
    options, args = parser.parse_args(argv)
    return options

if __name__ == "__main__":
    # Parse command line args
    ARGS = parse_args(sys.argv[1:])
    sys.exit(main(ARGS))

