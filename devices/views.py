from django.http import HttpResponse, JsonResponse
from .models import Device
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
def index(request):
    return HttpResponse("Hello, user!")

def get_device(request, device_id):
    device_object = get_object_or_404(Device, device_id=device_id)
    device = model_to_dict(device_object)
    responseStructure = {'success' : True, 'data' : device}
    return JsonResponse(responseStructure, safe=False)

@csrf_exempt
def create_device(request):
    if request.method != 'POST':
        return JsonResponse({'success' : False, 'msg' : 'Expected a POST method'})
    device_id = request.POST['device_id']
    device_name = request.POST['device_name']
    nickname = request.POST['nickname']
    controller = request.POST['controller']
    device_type = request.POST['device_type']
    correspondingRoom = Room.objects.get(room_id=room_id)
    try:
        Device.objects.create(device_id = device_id, name = device_name, nickname = nickname, controller = controller, device_type=device_type)
        device.save()
        responseStructure = {'success' : True, 'msg' : 'Device created successfully!'}
    except IntegrityError as e:
        responseStructure = {'success': False, 'msg' : 'Device ID already in use'}
    except Exception as e:
        print (e)
        responseStructure = {'success' : False, 'msg' : 'Invalid data format'}
    return JsonResponse(responseStructure, safe=False)

def get_all_devices(request):
    device_objects = list(Device.objects.all())
    devices = [model_to_dict(device) for device in device_objects]
    responseStructure = {'success' : True, 'data' : devices}
    return JsonResponse(responseStructure, safe=False)

def delete_device(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    device.delete()
    return JsonResponse({'success' : True, 'msg' : 'Device Deleted'})
