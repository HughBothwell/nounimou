# Skyfield working stuff
# https://rhodesmill.org/skyfield/files.html
from math import *
from skyfield import almanac, api

MOON_DIA      =      3475000    # meters

def moon_angle(dist):
    """
    Given a viewing distance in meters,
    return the Moon's subtended angle in radians
    """
    return 2. * asin(0.5 * MOON_DIA / dist)
    
def rad_to_degminsec(angle, fmt="{deg:01d}deg {min:01d}' {sec:0.1f}\""):
    """
    Given an angle in radians,
      return it as a degrees arcmin arcsec string
      where degrees is in [0 .. 360)
    """
    angle = degrees(angle) % 360.
    deg = int(angle)
    rem = 60. * (angle - deg)
    min_ = int(rem)
    sec = 60. * (rem - min_)
    return fmt.format(deg=deg, min=min_, sec=sec)

# load ephemeris data
load = api.Loader("d:/skyfield-data")   # set up data dir
data = load("de435.bsp")                # load JPL ephemerides

# set locations
earth  = data["Earth"]                  # Earth CoM
lex = api.Topos('35.65 N', '88.39 W')   # city offsets from Earth-center
zag = api.Topos('45.81 N', '15.98 W')
moon = data["Moon"]                     # Moon CoM

# set timescale
ts = load.timescale()
photo_time = ts.utc(2019, 2, 20, 4, 13)          # UTC time of Lexington photo

# find alt/az of Moon
lex_moon = (earth + lex).at(photo_time).observe(moon)
print("Lexington:", lex_moon.apparent().altaz("standard"))
print("Size:", rad_to_degminsec(moon_angle(lex_moon.distance().m)))

zag_moon = (earth + zag).at(photo_time).observe(moon)
print("Zagreb:", zag_moon.apparent().altaz("standard"))
print("Size:", rad_to_degminsec(moon_angle(zag_moon.distance().m)))
