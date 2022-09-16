from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string


# Create your views here.
def checkPasswordStrength(password):
    special_chars = list('@#$%&')
    isDigit_there = any(char.isdigit() for char in password)
    isUpper_there = any(char.isupper() for char in password)
    isLower_there = any(char.islower() for char in password)
    isSpecial_there = any(char in special_chars for char in password)
    
    all_true = all([isDigit_there, isUpper_there, isLower_there, isSpecial_there])
    
    if len(password)< 6:
        return 'weak'
    elif len(password)>6 and all_true:
        return 'strong'
    else:
        return 'medium'
    
class PasswordCheckerView(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password']
        
        pass_strength = checkPasswordStrength(password)
        if pass_strength == 'weak':
            return JsonResponse({'pass_strength': "Password too short"}, status = 400)
        if pass_strength == 'medium':
            return JsonResponse({'pass_strength': "Password Strength: Medium"})
        if pass_strength == 'strong':
            return JsonResponse({'pass_strength': "Password Strength: Strong"})
                
                    
            
        
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
    
    def post(self, request):
        # Get user data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        context = {
            'form' : request.POST,
        }

        # validate
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request,'Password too short')
                    return render(request, 'authentication/register.html', context)

                # create a user 
                user = User.objects.create_user(
                    username=username,
                    email= email,
                )
                user.set_password(password)
                user.is_active = False
                user.save()
                
                email_subject = 'Activate your acctount'
                email_body = 'Please verify your email address to activate your ERP account'
                sender_email = settings.EMAIL_HOST_USER
                receiver_email = email
                # email = EmailMessage( 
                #     email_subject,
                #     email_body,
                #     sender_email,
                #     [receiver_email],  
                # )
                # email.send(fail_silently=False)
                # # email.fail_silently=False
                # # email.send()
                send_mail(
                    email_subject, 
                    email_body, 
                    sender_email, 
                    [receiver_email],
                    fail_silently=False
                    )             
                
                messages.success(request, "Account created successfully")
                return render(request, 'authentication/register.html')
        
        return render(request, 'authentication/register.html')
