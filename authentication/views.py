from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.
class UserNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        print('request body : ', request.body)
        print('data here: ',data)
        username = data['username']
        print('username here: ',username)
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error':'Sorry username already exists, choose another one'}, status=400)
        return JsonResponse({'username_valid':True})  
    
class RedistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
