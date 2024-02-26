
from shelly import Shelly


shelly1 = Shelly()
shelly2 = Shelly()
shelly1.ip = '10.0.60.10'
shelly2.ip = '10.0.60.11'
print(shelly1.get_data())
print(shelly2.get_data())
