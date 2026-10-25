from skyfield.api import load

# Load timescale and current time
ts = load.timescale()
t-now = ts.now()

#Load the active space stations or satellites in the low earth orbit
url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle'
satellites = load.tle_file(url)

print(f"The files have been successfully loaded {len(satellites)} objects from NORAD.")
#Picking first two satellites for comparrision

sat_a = satellites[0]
sat_b = satellites[1]
#Pulling their x, y, z positions in kilometers at t_now

pos_a = sat_a.at(t_now).position.km
pos_b = sat_b.at(t_now).position.km
#Extract the x, y, z postions for sat_a

x1, y1, z1 = pos_a[0], pos_a[1], pos_a[2]
