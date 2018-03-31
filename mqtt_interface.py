import paho.mqtt.client as mqtt
import time, requests

flags = [False, False, False]

def on_connect(client, userdata, flags, rc):
    print ("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    global flags
    payload = msg.payload.decode("utf-8")
    values = payload.split(';')
    device_id = values[1]
    device_value = values[2]
    value_type = values[-1]
    if value_type == 'A':
        flags[0] = device_value
    elif value_type == 'M':
        flags[1] = device_value
        flags[2] = values[3]

    if False not in flags:
        requestStructure = {
            'lux_value' : flags[2],
            'temp_value' : flags[1],
            'device_id' : device_id,
            'value' : flags[0],
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
client.loop_forever()

