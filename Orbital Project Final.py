from skyfield.api import load
import math
import matplotlib.pyplot as plt

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

#Constants for the collision avoidance scenarios
SAFETY_BUBBLE_METERS = 5000.0 #Establishing a 5km clearance is required

#Weights for the optimization function balancing fuel cost vs. risk
W_FUEL = 1.0 #Priority on conserving thruster fuel
W_UNCERTAINTY = 0.8 #Making the penality for acting on blurry radar data

# Establishing lists tp store simmulation results to plot later
lead_times_min = []
delta_v_list = []
uncertainty_list = []
total_costs = []

best_lead_time = 0
lowest_cost = float('inf')

print("Simulating burn maneuvers from 10 to 120 minutes before the conjuction...\n")

#Loop through the burn lead times from 10 to 120 minutes
for lead_min in range (10, 121):
    #Converting minutes to seconds for accessible physics formulas
    lead_sec = lead_min * 60

    #Performing calculations
    dv = SAFETY_BUBBLE_METERS / lead_sec

    #Calculating radar uncertainty
    uncertainty_km = 0.2 + (0.04 * lead_min)

    #Calculate combined cost score
    cost = (W_FUEL * dv) + (W_UNCERTAINTY * uncertainty_km)

    #Store data in order to graph
    lead_times_min.append(lead_min)
    delta_v_list.append(dv)
    uncertainty_list.append(uncertainty_km)
    total_costs.append(cost)

    #Check if the cost is less than the lowest cost
    if cost < lowest_cost:
        lowest_cost = cost
        best_lead_time = lead_min

#Building a summary of the findings
print("Optimization outputs")
print(f"Optimal burn lead time: {best_lead_time} minutes prior to the encounter")
print(f"Lowest trade-off cost score: {lowest_cost:.3f}")

#Building a graph visualization of the optimization outputs
#Setting up two plots one on another
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8,7), sharex=True)

#Graph 1: Comparing fuel burn (delta v) vs radar uncertainty
ax1.plot(lead_times_min, delta_v_list, label='Delta V (Fuel Burn)', color='blue')
ax1.plot(lead_times_min, uncertainty_list, label='Radar uncertainty (km)', color='orange', linestyle='--')
ax1.set_ylabel('Values (m/s and km)')
ax1.set_title('Satellites maneuver: Fuel vs Radar Uncertainty')
ax1.grid(True)
ax1.legend()

#Graph 2: The plotting of combined trade-off cost function
ax2.plot(lead_times_min, total_costs, label='Combined cost', color='purple')
#Plotting the red dot as the most optimal time
ax2.scatter(best_lead_time, lowest_cost, color='red', s=50, label=f'optimal burn ({best_lead_time} mins)')
ax2.set_xlabel('Burn lead time (minutes before conunction)')
ax2.set_ylabel('Cost score')
ax2.grid(True)
ax2.legend()

#Making sure the labels dont overlap

plt.tight_layout()

#Saving a png to the folder so I can upload it to GITHUB
plt.savefig('tradeoff_curve.png')
print("Graph saved successfully as tradeoff_curve.png")

#Showing the plot screen
plt.show()
