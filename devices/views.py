from django.http import HttpResponse, JsonResponse
from .models import Device, Room
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
    wattage = int(request.POST['wattage'])
    device_name = request.POST['device_name']
    nickname = request.POST['nickname']
    usage_number = int(request.POST['usage_number'])
    room_id = request.POST['room_id']
    correspondingRoom = Room.objects.get(room_id=room_id)
    try:
        device = Device.objects.create(device_id = device_id, name = device_name, nickname = nickname, usage_number = usage_number, wattage = wattage, room = correspondingRoom)
        device.save()
        responseStructure = {'success' : True, 'msg' : 'Device created successfully!'}
    except IntegrityError as e:
        responseStructure = {'success': False, 'msg' : 'Device ID already in use'}
    return JsonResponse(responseStructure, safe=False)

def get_all_devices(request, room_id):
    room_object = get_object_or_404(Room, room_id=room_id)
    device_objects = list(Device.objects.filter(room=room_object))
    devices = [model_to_dict(device) for device in device_objects]
    room = model_to_dict(room_object)
    room['devices'] = devices
    responseStructure = {'success' : True, 'data' : room}
    return JsonResponse(responseStructure, safe=False)

def delete_device(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    device.delete()
    return JsonResponse({'success' : True, 'msg' : 'Device Deleted'})


def get_room(request, room_id):
    room_object = get_object_or_404(Room, room_id=room_id)
    room = model_to_dict(room_object)
    responseStructure = {'success' : True, 'data' : room}
    return JsonResponse(responseStructure, safe=False)


@csrf_exempt
def create_room(request):
    if request.method != 'POST':
        return JsonResponse({'success' : False, 'msg' : 'Expected a POST method'})
    room_id = request.POST['room_id']
    name = request.POST['name']
    try:
        room = Room.objects.create(room_id = room_id, name=name)
        room.save()
        responseStructure = {'success' : True, 'msg' : 'Room created successfully!'}
    except IntegrityError as e:
        responseStructure = {'success': False, 'msg' : 'Room ID already in use'}
    return JsonResponse(responseStructure, safe=False)

def get_all_rooms(request):
    rooms = list(Room.objects.all())
    responseStructure = {'success' : True, 'data' : []}
    for room_object in rooms:
        room = model_to_dict(room_object)
        device_objects = list(Device.objects.filter(room=room_object))
        devices = [model_to_dict(device) for device in device_objects]
        room['devices'] = devices
        responseStructure['data'].append(room)
    return JsonResponse(responseStructure, safe=False)

def delete_room(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    room.delete()
    return JsonResponse({'success' : True, 'msg' : 'Room deleted'})



