# Graph the variation in Earth-Moon distance over time

#   There are a bunch of different implementations of Python;
#   I happen to like Anaconda, https://www.anaconda.com/distribution/
#   it's a scientific-oriented version that has a lot of modules
#   precompiled for Windows which can otherwise be problematic to install.

# Skyfield docs at https://rhodesmill.org/skyfield/
#   install as: pip install skyfield
from skyfield import almanac, api
# Matplotlib docs at https://matplotlib.org/users/index.html
import matplotlib.pyplot as plt

# Load ephemeris data
load = api.Loader("d:/skyfield-data")       # which directory to store your BSP files in
#   BSP files are precomputed tables of planet location at time intervals,
#   prepared by JPL by numeric integration; skyfield can find very precise
#   planet locations at any time by interpolating between intervals.
#   You can get different files, covering different sets of planets and moons
#   at varying precision over varying periods; some of the files can get quite large.
# data = load("de421.bsp")                  # default base data set
data = load("de435.bsp")                    # Extended data set (higher precision over longer time period)
                                            # You may have to download this manually from JPL - about 114 MB
                                            # See https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/

# Init bodies
sun   = data["Sun"]
earth = data["Earth"]
moon  = data["Moon"]

# Set up a timescale (a date or list of dates)
#   skyfield likes vectorized operations for speed - instead of
#   saying "calculate for this date, then this date, then this date..."
#   it wants you to "calculate for [this list of dates]"
ts = load.timescale()
t1 = ts.utc(2015, 1, 1, range(0, int(9 * 365.25 * 24), 3))    # every 3 hours for 9 years (2015 to 2024)

#   Planet positions are tracked by barycenter;
#   for Earth observations, you have to specify your
#   location as a barycenter-offset, ie
# kingston = api.Topos('44.2312 N', '76.4860 W')
# mloc = (earth + kingston).at(t1).observe(moon).apparent()
#   For Earth-Moon distance, we don't need to care about that

# Find distance between Earth-barycenter and Moon-barycenter, for 25 years, in kilometers
moon_dist = earth.at(t1).observe(moon).distance().km

# Plot the results
xs = t1.utc_datetime()                      # convert skyfield timestamps back to Python datetimes for pyplot
plt.figure(figsize=(12,8))                  # set output file size in inches
plt.title("Earth-Moon distance (km)")       # set plot title
plt.plot(xs, moon_dist, "r-")               # plot as a red continuous line