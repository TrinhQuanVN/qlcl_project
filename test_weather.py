# Import Meteostat library and dependencies
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily

# Set time period
start = datetime(2021, 10, 1)
end = datetime(2021, 11, 1)

# Create Point for Vancouver, BC
location = Point(21.025821, 105.856541, 70)

# Get daily data for 2018
data = Daily(location, start, end)
data = data.fetch()
print(data)

# Plot line chart including average, minimum and maximum temperature
# data.plot(y=['tavg', 'tmin', 'tmax'])
# plt.show()