from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email

# Create your views here.
class UserNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body) 
        username = data['username']
        print('username here: ',username)
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error':'Sorry username already exists, choose another one'}, status=400)
        return JsonResponse({'username_valid':True})  
    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body) 
        email = data['email']
        print('email here: ',email)
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'}, status=400)
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error':'Sorry email already exists, choose another one'}, status=400)
        return JsonResponse({'email_valid':True})  
    
class RedistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
