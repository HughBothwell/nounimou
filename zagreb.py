# Skyfield working stuff
# https://rhodesmill.org/skyfield/files.html
from skyfield import almanac, api

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
lex_moon = (earth + lex).at(photo_time).observe(moon).apparent()
print("Lexington:", lex_moon.altaz("standard"))

zag_moon = (earth + zag).at(photo_time).observe(moon).apparent()
print("Zagreb:", zag_moon.altaz("standard"))
