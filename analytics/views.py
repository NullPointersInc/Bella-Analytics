from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from .models import LoggedDeviceData, LoggedRoomData
from devices.models import Device
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import matplotlib, base64, os, json
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import time
import numpy as np
from .ml import do_knn


#Set the mode to key if the corresponding controller has reading above the value
temp = {
    'F' : {
        2 : 30,
        1 : 20,
    },
    'B' : {
        1 : 24,
    }
}

#Set the mode to key if the corresponding controller has reading below the value
lum = {
        2 : 300,
        1 : 550,
    }


#Labels
labels = {
    'F' : {
        2 : '1',
        1 : 'P',
        0 : '0',
    },
    'B' : {
        1 : '1',
        0 : '0',
    }
}

state_labels = {
    0 : 'off',
    1 : 'partial',
    2 : 'on',
}

# Helper functions

def process(device, lux, temp, val, ts):
    state = device.state
    controller = device.controller
    device_type = device.device_type
    old_state = device.state
    if controller == 'T':
        allowed_temp = temp[controller][state]
        maxim = max(temp[controller].keys())
        minim = min(temp[controller].keys()) - 1
        new_state = state
# If temperature is greater than the maximum defined temperature
        if temp > temp[controller][maxim]:
            new_state = maxim
# If temperature is lesser than the minimum defined temperature
        elif temp < temp[controller][1]:
            new_state = 0
# Somewhere in the middle
        elif temp < allowed_temp:
            new_state = max(state-1, minim)
        elif temp > allowed_temp:
            new_state = min(state+1, maxim)

    elif controller == 'L':
# Lux sensors are room-specific and encompass devices
        lux_devices = list(Device.objects.filter(controller='L'))
# Bulbs are binary and activate at 2, ambients are 1 territory
        if lux < lum[2]:
            new_state = 2
        elif lux < lum[1]:
            new_state = 1
        else:
            new_state = 0

#H:3 if device 3 is high, L:3 if device 3 is low
    device_id = device.device_id
    if new_state > old_state:
        new_str = 'L'
    elif new_state < old_state:
        new_str = 'H'
    else:
        new_str='X'
    return (str(device_id) + ':' + new_str)


# Create your views here.

def index(request):
    return HttpResponse('Hello, user!')

@csrf_exempt
def log_data(request):
    if request.method != 'POST':
        return JsonResponse({'success' : False, 'msg' : 'Expected a POST method'})
    timestamp = int(request.POST['timestamp'])
    device_id = request.POST['device_id']
    value = int(request.POST['value'])
    response = attemptLogData(timestamp, device_id, value)
    if response:
        mess = 'Log successful'
    else:
        mess = 'Log failed!'
    return JsonResponse({'success' : response, 'msg' : mess})

def avg(lst):
    return sum(lst)/len(lst)

def get_last_turn_on(lst):
    x = len(lst) - 1
    if lst[x] < 0.4:
        return x
    x -=1
    while x >= 0:
        if lst[x] < 0.4:
            break
    return x+1

def get_stats(request):
    device_objs = list(Device.objects.all())
    devices = [model_to_dict(device) for device in device_objs]
    for device in devices:
        #current_usage
        #active_since
        #assisted_triggers
        #power consumed
        needed_log_objs = list(LoggedDeviceData.objects.filter(device = device_objs[devices.index(device)]))
        needed_logs = [model_to_dict(log) for log in needed_log_objs]
        amps = [ x['value'] for x in needed_logs ]
        latest_slice = get_last_turn_on(amps)
        tstamps = [ x['timestamp'] for x in needed_logs ]
        assisted_triggers = len(needed_logs)//2
        avg_current_use = avg(amps)
        active_since = tstamps[latest_slice]
        total_power_consumed = sum(amps)*0.23

        device['stats'] = {
            'current' : avg_current_use,
            'active_since' : active_since,
            'power_consumed' : total_power_consumed,
            'assisted_triggers' : assisted_triggers,
        }
    return JsonResponse({'success' : True, 'data' : devices})


'''
def attemptLogData(timestamp, device_id, value):
    try:
        device = get_object_or_404(Device, device_id=device_id)
        state = state_labels(device.state)
        logged_data = LoggedData.objects.create(timestamp = timestamp, device_id = device_id, value = value, state = state)
        logged_data.save()
        return True
    except Exception as e:
        return False
'''
def get_device_graph(request, device_id):
    device_object = get_object_or_404(Device, device_id=device_id)
    needed_logs = list(LoggedDeviceData.objects.filter(device=device_object).values('timestamp', 'value'))
    timestamps = [log['timestamp'] for log in needed_logs]
    values = [log['value'] for log in needed_logs]
    if len(values) < 1:
        return JsonResponse({'success' : False, 'msg' : 'No data to plot'})

    device = model_to_dict(device_object)
    plt.plot(timestamps, values, label=device['nickname'])
    plt.xlabel('Timestamps')
    plt.ylabel('Values')
    plt.legend(loc='best')
    now = datetime.now().isoformat()
    now = now[:now.index('.')]
    plt.savefig(now + device_id)
    with open(now + device_id + '.png', 'rb') as f:
        data = f.read()
    image_data = base64.encodestring(data)
    #os.remove(now + device_id + '.png')
    responseStructure = {'success' : True, 'data' : image_data.decode()}
    return JsonResponse(responseStructure, safe=False)

def get_room_graph(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    devices = list(Device.objects.filter(room=room).values('device_id'))
    for dev in devices:
        device_object = get_object_or_404(Device, device_id=dev['device_id'])
        needed_logs = list(LoggedDeviceData.objects.filter(device=device_object).values('timestamp', 'value'))
        timestamps = [log['timestamp'] for log in needed_logs]
        values = [log['value'] for log in needed_logs]
        device = model_to_dict(device_object)
        plt.plot(timestamps, values, label=device['nickname'])
    plt.xlabel('Timestamps')
    plt.ylabel('Values')
    plt.legend(loc='best')
    now = datetime.now().isoformat()
    now = now[:now.index('.')]
    plt.savefig(now + room_id)
    with open(now + room_id + '.png', 'rb') as f:
        data = f.read()
    image_data = base64.encodestring(data)
    #os.remove(now + room_id + '.png')
    responseStructure = {'success' : True, 'data' : image_data.decode()}
    return JsonResponse(responseStructure, safe=False)

@csrf_exempt

def handle_live_data(request):
    lum_max = 950

    hum_value = request.POST.get("hum_value", 0)
    lux_value = float(request.POST.get("lux_value", 0))
    temp_value = float(request.POST.get("temp_value", 0))
    timestamp = float(request.POST.get("timestamp", 0))
    lum_devices = list(Device.objects.filter(controller = 'L'))
    returnableStringList = []
    for device in lum_devices:
        usage = device.mean_usage*device.state + np.random.normal(loc=0.2, scale=0.01)
        ldd = LoggedDeviceData(timestamp = timestamp, device = device, value = usage, state = device.state)
        ldd.save()
        payload = process(device, lux_value, temp_value, usage, timestamp)
        if payload.find("X") == -1:
            returnableStringList.append(payload)

    temp_devices = list(Device.objects.filter(controller = 'T'))
    for device in temp_devices:
        usage = device.mean_usage*device.state + np.random.normal(loc=0.2, scale=0.01)
        ldd = LoggedDeviceData(timestamp = timestamp, device = device, value = usage, state = device.state)
        ldd.save()
        payload = process(device, lux_value, temp_value, usage, timestamp)
        if payload.find("X") == -1:
            returnableStringList.append(payload)

    hum_devices = list(Device.objects.filter(controller = 'H'))
    for device in hum_devices:
        usage = device.mean_usage*device.state + np.random.normal(loc=0.2, scale=0.01)
        ldd = LoggedDeviceData(timestamp = timestamp, device = device, value = usage, state = device.state)
        ldd.save()
        payload = process(device, lux_value, temp_value, usage, timestamp)
        if payload.find("X") == -1:
            returnableStringList.append(payload)





# Log values for device only
    nearby_lrds = LoggedRoomData.objects.filter(timestamp__gte=timestamp-10)
    if nearby_lrds.count() < 1:
        lrd = LoggedRoomData(timestamp = timestamp, lux_value = lux_value, temp_value = temp_value, hum_value = hum_value)
        lrd.save()
    returnableString = ':'.join(returnableStringList)
    return JsonResponse({'success' : True, 'payload' : returnableString})


def perform_anomaly_detection(request):
    devices = list(Device.objects.all())
    accuracies = {}
    for device in devices:
        accuracy = do_knn(device.device_id)
        accuracies[device.device_id] = accuracy
    return JsonResponse({'success' : True, 'data' : accuracies})





def handle_live_data2(request):
    room_id = request.POST['room_id']
    devices = json.load(request.POST.get('devices', []))
    lux = float(request.POST.get('lux_value', 0))
    temp = float(request.POST.get('temp_value', 0))
    timestamp = int(time.time())
    payload_list = []
    now_hrs = int(datetime.fromtimestamp(timestamp).strftime('%H'))
    for device_id, value in devices.items():
        val = float(value)
        attemptLogData(timestamp, device_id, val)
        #Handler for devices dependent on lux
        device_model = get_object_or_404(Device, device_id = device_id)
        device = model_to_dict(device_model)
        device_type = device['device_type']
        controller = device['controller']
        state = device['state']
        if controller == 'L':
            if lux > max(lum[controller].values()):
                new_state = 0
            elif lux < min(lum[controller].values()):
                new_state = max(lum[controller].keys())
           # elif lum_map[state] > time['L'][device_type][now_hrs]:
            #    new_state = time['L'][now_hrs]
            else:
                expected_lux = lum[controller][state]
                if lux > expected_lux:
                    new_state = lum[controller][min(state-1, 0)]
                elif lux < expected_lux:
                    new_state = lum[controller][max(state+1, max(lum[controller].keys()))]

        if controller == 'T':
            if temp < min(temp[controller].values()):
                new_state = 0
            elif temp > max(temp[controller].values()):
                new_state = max(temp[controller].keys())
            else:
                expected_temp = temp[controller][state]
                if temp < expected_temp:
                    new_state =temp[controller][min(state-1, 0)]
                elif temp > expected_temp:
                    new_state = temp[controller][max(state+1, max(temp[controller].keys()))]
        payload_list.append(device_id)
        payload_list.append(labels[state])
        payload_list.append(labels[new_state])
        device_model.next_state = new_state
        device_model.save()

    payload = ';'.join(payload_list)
    return JsonResponse({'success' : True, 'payload' : payload})


def update_success(request, device_id):
    device = get_object_or_404(Device, device_id = device_id)
    device.state = device.next_state
    device.save()
    return JsonResponse({'success' : True})
