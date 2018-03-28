from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from .models import LoggedData
from devices.models import Device, Room
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import matplotlib, base64, os
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

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
    try:
        logged_data = LoggedData.objects.create(timestamp = timestamp, device_id = device_id, value = value)
        logged_data.save()
        responseStructure = {'success' : True, 'msg' : 'Log successful!'}
    except Exception as e:
        responseStructure = {'success' : False, 'msg' : 'Could not save log!'}
    return JsonResponse(responseStructure, safe=False)

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


