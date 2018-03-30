import paho.mqtt.client as mqtt
import time, requests

def on_connect(client, userdata, flags, rc):
    print ("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
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
        for i in range(0, len(values[2:-2]):
            device_id = room_id + 'r' + str(i+1)
            value = values[2+i]
            requestStructure['devices'].append({device_id : value})
            
        r = requests.post("0:8000/analytics/log_data_live", data = requestStructure)
        response = r.json()
        payload = response['payload']
        client.publish('bellax/ack', payload)

    elif payload[1] == "T":
        device_id = '1r' + payload[0]
        queryUrl = "0:8000/analytics/update_success" + device_id
        r = requests.put(queryUrl)

        


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('astr1x', password='astr1x2096')
client.connect("192.168.43.233", 1883, 60)
client.subscribe("bellax/ack")
client.loop_forever()

