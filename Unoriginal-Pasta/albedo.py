import math

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
    ice = 0.7
    water = 0.2
    meltpoint = 273.15
    variance = 10

    return (water-ice)*g((t-(meltpoint-variance))/(2*variance))+ice
