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
   ' L' : [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 1, 1],
}

temp = {
    'T' : {
        30 : 3,
        24 : 2,
        20 : 1,
    }

}

lum = {
    'L' : {
        300 : 2,
        500 : 1,
        700 : 0,
    }
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
        logged_data = LoggedData.objects.create(timestamp = timestamp, device_id = device_id, value = value)
        logged_data.save()
        return True
    except Exception as e:
        return False

def get_device_graph(request, device_id):
    needed_logs = list(LoggedData.objects.filter(device_id=device_id).values('timestamp', 'value'))
    timestamps = [log['timestamp'] for log in needed_logs]
    values = [log['value'] for log in needed_logs]
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
    timestamp = int(time.time())
    for device_id, value in devices.items():
        attemptLogData(timestamp, device_id, value)
    now_hrs = int(datetime.fromtimestamp(timestamp).strftime('%H'))
    



    


