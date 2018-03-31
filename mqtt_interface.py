import paho.mqtt.client as mqtt
import time, requests, threading

flags = [False, False, False]

strs = [
    'H:1T',
    'H:1F',
    'H:1A',
    'H:1B',
    'H:2T',
    'H:2F',
    'H:2A',
    'H:2B',
    'H:3T',
    'H:3F',
    'H:3A',
    'H:3B',
    '4T:',
    '4F:',
    '4A:',
    '4B:',
]

def on_connect(client, userdata, flags, rc):
    print ("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    global flags
    payload = msg.payload.decode("utf-8")
    values = payload.split(';')
    '''
        S;L
        S;T
        S;H

        S;L;123
        S;T;456
        S;H;789
    '''
    if values[0] == 'S':
        if values[1] == 'L': #Light
            flags[2] = values[2]
        elif values[1] == 'T': #Temperature
            flags[1] = values[2]
        elif values[2] == 'H': #Humidity
            flags[0] = values[2]

    if False not in flags:
        now = int(time.time())
        requestStructure = {
            'lux_value' : flags[2],
            'temp_value' : flags[1],
            'timestamp' : now,
            'hum_value' : flags[0],
        }
        r = requests.post("http://0:8000/analytics/log_data_live", data=requestStructure)
        print("Received Response " + str(r))
        flags = [False, False, False]


def on_message2(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    if payload[0] == "S":
        room_id = payload[2]
        values = payload[2:].split(';')
        lux_value = values[:-1]
        temp_value = values[:-2]
        requestStructure = {
            'room_id' : room_id,
            'lux_value' : lux_value,
            'temp_value' : temp_value,
            'devices' : [],
        }
        for i in range(0, len(values[2:-2])):
            device_id = room_id + 'r' + str(i+1)
            value = values[2+i]
            requestStructure['devices'].append({device_id : value})

        r = requests.post("http://0:8000/analytics/log_data_live", data = requestStructure)
        print ("Received response " + str(r))
        response = r.json()
        payload = response['payload']
        client.publish('bellax/ack', payload)

    elif payload[1] == "T":
        device_id = '1r' + payload[0]
        queryUrl = "htp://0:8000/analytics/update_success" + device_id
        r = requests.put(queryUrl)
        print ("Received response " + str(r))



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('astr1x', password='astr1x2096')
client.connect("192.168.43.233", 1883, 60)
client.subscribe("bellax/ack")
print ("Subscribed to topic bellax/ack")

def poll_temp():
    client.publish('bellax/req', 'S;T')
    threading.Timer(10, poll_temp).start()

def poll_humd():
    client.publish('bellax/req', 'S;H')
    threading.Timer(10, poll_humd).start()

def poll_lum():
    client.publish('bellax/req', 'S;L')
    threading.Timer(10, poll_lum).start()

def poll_change():
    client.publish('bellax/req', 'S;L')
    threading.Timer(10, poll_lum).start()

poll_temp()
poll_humd()
poll_lum()
poll_change()
