# Jimmy ephemeris calculations -
# angle between Polaris and the Sun
import datetime
import ephem                # PyEphem - calculate ephemerides
import ephem.stars          # star catalog
from math import degrees

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

#
# Set up bodies for observation
#

# major body
SUN = ephem.Sun()

# from star catalog
POL = ephem.stars.stars["Polaris"]

# location on Earth
JIMMY = ephem.Observer()
JIMMY.lat = "33.885829"                     # as string (degrees North latitude)
JIMMY.lon = "-117.818459"                   # as string (degrees East longitude)
JIMMY.elevation = 111.3 + 1.5               # as float  (meters ASL)
JIMMY_TZ = datetime.timedelta(hours = -8)   # timezone offset (PST)

def update(utc_date_time):
    """
    Compute locations at given date and time
    """
    JIMMY.date = utc_date_time
    POL.compute(JIMMY)
    SUN.compute(JIMMY)
    
def show():
    """
    Display results
    """
    lt = JIMMY.date.datetime() + JIMMY_TZ   # cast back to Jimmy-local datetime
    sep = ephem.separation(SUN, POL)        # find separation angle
    print("""
At {timestamp} (Jimmy time):
Polaris is at heading {pol_az:0.2f}°, angle {pol_alt:0.2f}°
Sun is at heading {sun_az:0.2f}°, angle {sun_alt:0.2f}°
They are {sep:0.2f}° apart.
    """.format(
        timestamp = lt.strftime(TIME_FORMAT),
        pol_az = degrees(POL.az),
        pol_alt = degrees(POL.alt),
        sun_az = degrees(SUN.az),
        sun_alt = degrees(SUN.alt),
        sep = degrees(sep)
    )
    )
    
def main():
    while True:
        print("Please enter a Jimmy-local time as yyyy mm dd hh mm ss (or just hit Enter to quit):")
        ts = [int(wd) for wd in input().split()]
        if ts:
            dt = datetime.datetime(*ts) - JIMMY_TZ  # as UTC
            update(dt)
            show()
        else:
            break

if __name__ == "__main__":
    main()