import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt

POL = 6356000.      # meters
EQU = 6378000.
D_LAT = 0.001      # offset in degrees == about 110 meters

def find_y(x):
    """
    Find a point on the first quadrant of an ellipse
    """
    if x <= 0.:
        return POL
    elif x >= EQU:
        return 0.
    else:
        esq = EQU ** 2.
        return (esq - x ** 2.) ** 0.5 * POL / EQU
    
def find_xy(angle):
    """
    Find a point (x, y) on the ellipse at the given proper angle (radians)
    """
    # initial estimate
    x0 =  (POL + EQU) / 2. * np.cos(angle)
    # error fn
    def err(x, angle = angle):
        y = find_y(x)
        res = np.arctan2(y, x)
        return res - angle
    x = opt.root_scalar(err, x0 = x0, x1 = x0 + 0.1).root
    return (x, find_y(x))

    
def find_circle(x1, y1, x2, y2, x3, y3):
    """
    Returns the center and radius of the circle passing the given 3 points.
    In case the 3 points form a line, returns (None, infinity).
    """
    temp = x2 * x2 + y2 * y2
    bc = (x1 * x1 + y1 * y1 - temp) / 2
    cd = (temp - x3 * x3 - y3 * y3) / 2
    det = (x1 - x2) * (y2 - y3) - (x2 - x3) * (y1 - y2)

    if abs(det) < 1.e-8:
        return (None, np.inf)

    # Center of circle
    cx = (bc*(y2 - y3) - cd*(y1 - y2)) / det
    cy = ((x1 - x2) * cd - (x2 - x3) * bc) / det

    radius = np.sqrt((cx - x1) ** 2. + (cy - y1) ** 2.)
    return (cx, cy), radius
    
def main():
    lats = np.linspace(0.2, 89.8, 100)    # latitudes to measure at, in degrees

    xys_m = [find_xy(theta) for theta in np.radians(lats - D_LAT)]
    xys   = [find_xy(theta) for theta in np.radians(lats)]
    xys_p = [find_xy(theta) for theta in np.radians(lats + D_LAT)]

    rads = [find_circle(x1, y1, x2, y2, x3, y3)[1] for (x1, y1), (x2, y2), (x3, y3) in zip(xys_m, xys, xys_p)]
    rads[0] = rads[1]    # ? some sort of numerical precision error
    
    rads = np.array(rads)
    prop = 50983891.2    # constant of proportionality = 1609.34 m/mi * 5280 * 12 in/mi / 2
    ks = prop / rads     # so k is the constant at each latitude in in/mi^2
    
    # Now plot the result
    plt.figure(figsize=(12,8))              # set output file size in inches
    plt.title("Inches per miles-squared curvature constant by latitude")       # set plot title
    plt.plot(lats, ks, "b-")                # plot as a blue continuous line

if __name__ == "__main__":
    main()