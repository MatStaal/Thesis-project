import matplotlib

import matplotlib.pyplot as plt
import math
from matplotlib.ticker import NullFormatter
import numpy
import sys
    
def f(t):
    """
    Smooth Non-analytic function
    """
    if t <= 0:
        return 0
    else:
        return math.e**(-1/t)
        
def g(t):
    """
    Modified Smooth Non-analytic function
    """
    return f(t)/(f(t)+f(1-t))
    
def albedo(t):
    """
    Albedo using Smooth Non-analytic function
    """
    ice = 0.55
    water = 0.3
    meltpoint = 273.15
    variance = 10

    return (water-ice)*g((t-(meltpoint-variance))/(2*variance))+ice
    
def Secant(f,df,x0,x1,tol,iter):

    xnm1 = x1
    xnm2 = x0    
    
    for i in range(0,iter):
        xn = xnm1 - f(xnm1,df)*(xnm1-xnm2)/(f(xnm1,df)-f(xnm2,df))
        xnm2 = xnm1
        xnm1 = xn
        
        if abs(f(xn,df))<tol:
            return xn
            
    print("Solution not found")
    return None

def extrema(ls):
    res=[]
    if ls[1]-ls[0]<0:
        delta = False
    else:
        delta = True
        
    for i in range(1,len(ls)-2):
        if not delta and ls[i+1]-ls[i]>0:
            res.append((i,i+1))
            delta = True
        elif delta and ls[i+1]-ls[i]<0:
            res.append((i,i+1))
            delta = False
    
    return res
    
def csvtoplot(file, maxdf):
    res = [[],[]]
    f = open(file, 'r')
    for line in f:
        str = line.split(",")
        if float(str[0])<=maxdf:
            res[0].append(float(str[0]))
            res[1].append(float(str[1]))
            
    return res
    
def emptytuples(ls):
    res = []
    for i in range(0,len(ls)+1):
        res.append([[],[]])
    return res
    
def rootguess(ls):
    res = []
    for i in range(0,len(ls)-2):
        if ls[i]*ls[i+1] < 0:
            res.append((i,i+1))
    return res
    
def rootexact(rootls,df):
    res = []
    for el in rootls:
        res.append(Secant(model, df, el[0], el[1],10**(-9), 50))
    return res        
        
def model(T,df):
    S = 1367
    alpha = albedo(T)
    sigma = 5.670374419*10**(-8)
    epsilon = 0.612
    
    return (S*(1-alpha)/4-epsilon*sigma*T**4)+df
    
if __name__ == "__main__":
    # Euler
    #ET11, EY11 = Euler(0.1, f, 0, 1, 1)
    #ET12, EY12 = Euler(0.01, f, 0, 1, 1)
    #ET13, EY13 = Euler(0.001, f, 0, 1, 1)
    
    # RK4
    #ET21, EY21 = RK4(0.1, f, 0, 1, 1)
    #ET22, EY22 = RK4(0.01, f, 0, 1, 1)
    #ET23, EY23 = RK4(0.001, f, 0, 1, 1)
    
    min = 200
    max = 370
        
    X = numpy.linspace(min,max,(max-min)*1000+1)
    Y = [model(T,0) for T in X]
    plt.plot(X,Y, 'b') 
    #plt.plot(X,Y2, 'r') 
    plt.grid(True)
    plt.show()
    #Y = [albedo(t) for t in X]
    
    test = extrema(Y)
    test = [min+el[1]/1000 for el in test]
    
    deltaFmin = -30
    deltaFmax = 30
    deltaFarray = numpy.linspace(deltaFmin,deltaFmax,(deltaFmax-deltaFmin)*10+1)
    
    solutions = emptytuples(test)
    ls05 = csvtoplot("05.csv",30)
    ls10 = csvtoplot("10.csv",30)
    ls15 = csvtoplot("15.csv",30)
    
    for df in deltaFarray:
        newY = [el+df for el in Y]
        roots = rootguess(newY)
        roots = [(min+el[0]/1000,min+el[1]/1000) for el in roots]
        exact = rootexact(roots,df)
        print(round(df/deltaFmax*100, 1), end='\r')
        sys.stdout.flush()
        
        for y in exact:
            added = False
            for l in range(0,len(test)):
                if y < test[l]:
                    solutions[l][0].append(df)
                    solutions[l][1].append(y)
                    added = True
                    break
            
            if not added:
                solutions[len(test)][0].append(df)
                solutions[len(test)][1].append(y)
                    
    
    
    plt.plot(ls05[0],ls05[1], "orange")
    plt.plot(ls10[0],ls10[1], "g")
    plt.plot(ls15[0],ls15[1], "r")
    for el in solutions:
        if el[1][0] < el[1][1]:
            plt.plot(el[0],el[1], "b")
        else:
            plt.plot(el[0],el[1], "--b")
    
    
    
    # Guess where possible roots may be and convert them into readable X-values
    #roots = rootguess(Y)
    #roots = [(min+el[0]/1000,min+el[1]/1000) for el in roots]
    
    # Exact X-values
    #exact = rootexact(roots)
    

    #plotlength = X
    #plt.figure(1, figsize=((10 + math.log(plotlength)), 6))
    
    #plt.ylabel("Albedo")
    # plt.xlabel("Temperature (K)")
    # plt.plot(X,Y, 'b') 
    plt.grid(True)

    # `NullFormatter`, to avoid cumbering the axis with too many labels.
    #plt.gca().yaxis.set_minor_formatter(NullFormatter())
    #plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.45,
    #                    wspace=(0.50 / (math.log(plotlength) * 0.4)))

    plt.show()
    print("")