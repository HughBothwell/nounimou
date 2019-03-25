# Find the relative acceleration of the Moon due to the Sun and Earth
from skyfield import almanac, api
import matplotlib.pyplot as plt

# load ephemeris data
load = api.Loader("d:/skyfield-data")       # save-data directory
data = load("de435.bsp")                    # Note: you may have to download this manually from JPL.
                                            #       Large file - about 114 MB.
# init bodies
sun   = data["Sun"]
earth = data["Earth"]
moon  = data["Moon"]

# set up timescale
ts = load.timescale()
t1 = ts.utc(2018, 3, range(24, 24+365))     # 2018/03/24 to 2019/03/23 = 365 days

# find accelerations
sun_locs = moon.at(t1).observe(sun)
sun_gm = 1.327e20
sun_acc = sun_gm / sun_locs.distance().m ** 2.

earth_locs = moon.at(t1).observe(earth)
earth_gm = 3.986e14
earth_acc = earth_gm / earth_locs.distance().m ** 2.

# plot the results
xs = t1.utc_datetime()
plt.plot(xs, sun_acc, "r-", xs, earth_acc, "b-")