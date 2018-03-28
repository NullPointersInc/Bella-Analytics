from django.http import HttpResponse, JsonResponse
from .models import User
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Hello, user!")

def get_user(request, username):
    user_object = get_object_or_404(User, user_name=username)
    user = model_to_dict(user_object)
    responseStructure = {'success' : True, 'data' : user}
    return JsonResponse(responseStructure, safe=False)

@csrf_exempt
def create_user(request):
    if request.method != 'POST':
        return JsonResponse({'success' : False, 'msg' : 'Expected a POST method'})
    username = request.POST['username']
    fullname = request.POST['fullname']
    password = request.POST['password']
    user = User.objects.create(user_name = username, full_name = fullname, password = password)
    try:
        user.save()
        responseStructure = {'success' : True, 'msg' : 'User created successfully!'}
    except IntegrityError:
        responseStructure = {'success': False, 'msg' : 'Username already Taken'}
    return JsonResponse(responseStructure, safe=False)

def get_all(request):
    users = list(User.objects.values('user_name', 'full_name'))
    responseStructure = {'success' : True, 'data' : users}
    return JsonResponse(responseStructure, safe=False)
