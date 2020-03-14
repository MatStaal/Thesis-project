import matplotlib

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import math
from matplotlib.ticker import NullFormatter
import numpy
import sys

def csvtoplot(file, maxdf):
    """
    Given a csv file and max df we want, returns two lists of X- and Y-values.
    Input: File location, maxdf
    Output: 
    """
    res = [[],[]]
    f = open(file, 'r')
    for line in f:
        str = line.split(",")
        if float(str[0])<=maxdf:
            res[0].append(float(str[0]))
            res[1].append(float(str[1]))
            
    f.close()
    return res
    
def emptytuples(n):
    """
    Creates a list of empty tuples for the bifurcation diagram.
    Input: Integer n, read from the file
    Output: List of tuples
    """
    res = []
    for i in range(0,n+1):
        res.append([[],[]])
    return res
    
if __name__ == "__main__":
    # List for df growths 0.5, 1.0 and 1.5
    ls05 = csvtoplot("05.csv",30)
    ls10 = csvtoplot("10.csv",30)
    ls15 = csvtoplot("15.csv",30)
    
    # All of this to read the fixed bifurcation parameter into plottable list
    f = open("notime.csv","r")
    sol = emptytuples(int(f.readline()))
    counter = 0
    for line in f:
        if line == "\n":
            counter += 1
        else:
            str = line.split(",")
            sol[counter][0].append(float(str[0]))
            sol[counter][1].append(float(str[1]))
    
    
    plt.plot(ls05[0],ls05[1], "orange", label="a=0.5")
    plt.plot(ls10[0],ls10[1], "g", label="a=1.0")
    plt.plot(ls15[0],ls15[1], "r", label="a=1.5")
    for el in sol:
        # Ridiculously hacky way of plotting the bifurcation diagram with 
        # striped lines for when dT/dt is positive
        if el[1][0] < el[1][1]:
            plt.plot(el[0],el[1], "b")#, label="Fixed Stable")
        else:
            plt.plot(el[0],el[1], "--b")#, label="Fixed Unstable")
       
    plt.legend()
    plt.xlabel("Δf")
    plt.ylabel("Temperature (K)")
    plt.grid(True)
    plt.show()