from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from .models import LoggedData
from devices.models import Device, Room
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import matplotlib, base64, os, json
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import time

time = {
   ' L' : {
       'F' : [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
       'B' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0], 
    }
}


#Set the mode to key if the corresponding controller has reading above the value
temp = {
    'F' : {
        2 : 30,
        1 : 24,
    },
    'B' : {
        1 : 34,
    }
}

#Set the mode to key if the corresponding controller has reading below the value
lum = {
    'F' : {
        2 : 300,
        1 : 500,
    },
    'B' : {
        1 : 500
    }

}

lum_map = {
    'F' : 1,
    'B' : 2
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

def attemptLogData(timestamp, device_id, value):
    try:
        device = get_object_or_404(Device, device_id=device_id)
        state = state_labels(device.state)
        logged_data = LoggedData.objects.create(timestamp = timestamp, device_id = device_id, value = value, state = state)
        logged_data.save()
        return True
    except Exception as e:
        return False

def get_device_graph(request, device_id):
    needed_logs = list(LoggedData.objects.filter(device_id=device_id).values('timestamp', 'value'))
    timestamps = [log['timestamp'] for log in needed_logs]
    values = [log['value'] for log in needed_logs]
    if len(values) < 1:
        return JsonResponse({'success' : False, 'msg' : 'No data to plot'})
    device_object = get_object_or_404(Device, device_id=device_id)
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
    os.remove(now + device_id + '.png')
    responseStructure = {'success' : True, 'data' : image_data.decode()}
    return JsonResponse(responseStructure, safe=False)

def get_room_graph(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    devices = list(Device.objects.filter(room=room).values('device_id'))
    for dev in devices:    
        needed_logs = list(LoggedData.objects.filter(device_id=dev['device_id']).values('timestamp', 'value'))
        timestamps = [log['timestamp'] for log in needed_logs]
        values = [log['value'] for log in needed_logs]
        device_object = get_object_or_404(Device, device_id=dev['device_id'])
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
    os.remove(now + room_id + '.png')
    responseStructure = {'success' : True, 'data' : image_data.decode()}
    return JsonResponse(responseStructure, safe=False)

def handle_live_data(request):
    room_id = request['room_id']
    devices = json.load(request['devices'])
    lux = float(request['lux_value'])
    temp = float(request['temp_value'])
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

