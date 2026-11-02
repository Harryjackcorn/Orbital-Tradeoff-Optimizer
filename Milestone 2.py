from skyfield.api import load
import math

# Load timescale and current time
ts = load.timescale()
t_now = ts.now()

#Load the active space stations or satellites in the low earth orbit
url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle'
satellites = load.tle_file(url)

print(f"The files have been successfully loaded {len(satellites)} objects from NORAD.")
#Picking first two satellites for comparrision

sat_a = satellites[0]
sat_b = None
for s in satellites:
    if "TIANHE" in s.name or "CSS" in s.name:
        sat_b = s
        break

#If the CSS can't be found pull other satellite
if sat_b is None:
    sat_b = satellites[5]
#Pulling their x, y, z positions in kilometers at t_now

pos_a = sat_a.at(t_now).position.km
pos_b = sat_b.at(t_now).position.km
#Extract the x, y, z postions for sat_a

x1, y1, z1 = pos_a[0], pos_a[1], pos_a[2]

#Extract ther x, y, z positions for sat_b

x2, y2, z2 = pos_b[0], pos_b[1], pos_b[2]

#Calculate the 3d sitance between sat_a and sat_b

distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

#Printing the results
print(f"{sat_a.name} is {distance:.2f} km away from {sat_b.name}")

#Moving to calculating potential conjunctions
from datetime import datetime, timedelta, timezone

# Get the current UTC time
start_time = datetime.now(timezone.utc)

#Making an addition of 60 minutes to the start time
future_time = start_time + timedelta(minutes=60)

#Now convert the future time into a skyfield timescale object
t_future = ts.utc(future_time)

#Import necessary modules
from skyfield.api import load
from datetime import datetime, timedelta, timezone

#Intialize timescale and load stations data
ts = load.timescale()
satellites = load.tle_file(url)


#The current starting time in UTC
start_time = datetime.now(timezone.utc)

# Variables to store closest encounter found
min_distance = float('inf')
closest_minute = 0
closest_time_str = ""

print(f"Scanning 24-hour window (1440 minutes) for conjuctions between:")
print(f"Target A: {sat_a.name}")
print(f"Target B: {sat_b.name}\n")

#Loop through each minute of the next 24 hours (1440 minutes)
for minute in range(1440):
    sim_time = start_time + timedelta(minutes=minute)
    t = ts.utc(sim_time)

    #Get 3d Cords
    pos_a = sat_a.at(t).position.km
    pos_b = sat_b.at(t).position.km

    x1, y1, z1 = pos_a[0], pos_a[1], pos_a[2]
    x2, y2, z2 = pos_b[0], pos_b[1], pos_b[2]
    current_dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    if current_dist < min_distance:
        min_distance = current_dist
        closest_minute = minute
        closest_time_str = sim_time.strftime("%Y-%m-%d %H:%M:%S UTC")
print(f"The minimun distance found was: {min_distance:.2f} km")
print(f"This minimun distance occurs at: {closest_minute} minutes from the start time")
print(f"Timestamp is: {closest_time_str}")
        

    
