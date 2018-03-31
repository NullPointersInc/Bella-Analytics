import requests
big = 1.2
small = 0.7
import numpy as np
lux_thresh = 200
temp_thresh = 24
big_id = 1
small_id = 2
import time

luxs = [100, 100, 100, 100, 150, 300, 500, 500, 500, 500, 600, 600, 600, 650, 650, 650, 650, 600, 400, 100, 100, 100, 100, 100]
temps = [31, 30, 30, 29, 28, 28, 27, 29, 30, 31, 33, 35, 38, 39, 39, 40, 39, 39, 38, 36, 34, 33, 32, 31]
hums = [(temp + 10)/2 for temp in temps]

now = time.time()

for i in range(0, 50):
    timestamp = now + i*3600
    temp = temps[i%24]
    lux = luxs[i%24]
    hum_value = hums[i%24]
    state = (1 if lux > lux_thresh else 0)
    if np.random.normal(loc=0, scale=0.7) > 0.1:
        state = 1-state
    value = (big)*state + np.random.normal(loc=0.2, scale=0.01)
    requestStructure = {
        'lux_value' : lux,
        'temp_value' : temp,
        'hum_value' : hum_value,
        'timestamp' : timestamp,
    }
    r = requests.post("http://0:8000/analytics/log_data_live", data=requestStructure)
    value = (small)*state + np.random.normal(loc=0.1, scale=0.05)
    requestStructure = {
        'lux_value' : lux,
        'temp_value' : temp,
        'device_id' : small_id,
        'timestamp' : timestamp,
        'value' : value,
    }
    r = requests.post("http://0:8000/analytics/log_data_live", data=requestStructure)
