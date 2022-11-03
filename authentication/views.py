from ast import Expression
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import account_activation_token
from django.utils.encoding import force_str as force_text
from django.contrib import auth
import threading

# Create your views here.
class EmailThread(threading.Thread):
    
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send(fail_silently = False)
    

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
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not account_activation_token.check_token(user, token):
                print('******************1')
                return render('login'+'?message='+'User already activated')
            
            if user.is_active:
                print('******************2')
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request,'Account successfully activated')
            print('******************3')
            return redirect('login')
        
        except Exception as e:
            pass
          
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +user.username+' you are now logged in')
                    return redirect('expenses')
                
                messages.error(request, 'Account is not active, Please check your email.')
                return render(request, 'registration/login.html')
            
            messages.error(request, 'Invalid credentials, Try again.')
            return render(request, 'registration/login.html')
        
        messages.error(request, 'Please fill all the fields')
        return render(request, 'registration/login.html')
    
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
        return render(request, 'registration/register.html')
    
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
                    return render(request, 'registration/register.html', context)

                # create a user 
                user = User.objects.create_user(
                    username=username,
                    email= email,
                )
                user.set_password(password)
                user.is_active = False
                user.save()
                
                
                # - path to view
                # - getting domain we are on
                # - relative url to verificaion 
                # - encode uid
                # - token
                domain = get_current_site(request).domain
                print(f'domain here : {domain}')
                
                print('I am in Utils : ', account_activation_token)
                print('Token generated make token : ',account_activation_token.make_token(user))
                
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
                print(f'reverse link here: {link}')
                activate_url = 'http://'+domain+link


                
                email_subject = 'Activate your acctount'
                email_body = 'Hi '+user.username+'\nPlease verify your email address to activate your ERP account\n'+activate_url
                sender_email = settings.EMAIL_HOST_USER
                receiver_email = email
                
                try:
                    email = send_mail(
                        email_subject, 
                        email_body, 
                        sender_email, 
                        [receiver_email],
                        fail_silently=False
                    )
                    
                    # EmailThread used to send email faster
                    EmailThread(email).start()             
                    # send_mail(
                    #     email_subject, 
                    #     email_body, 
                    #     sender_email, 
                    #     [receiver_email],
                    #     fail_silently=False
                    # )             
                    messages.success(request, "Account created successfully")
                except Exception as e:
                    return False
                                    
                return render(request, 'registration/register.html')
        
        return render(request, 'registration/register.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
    
# class RequestPasswordResetEmailView(View):
#     def get(self, request):
#         return render(request, 'registration/reset-password.html')
    
#     def post(self, request):
#         return render(request, 'registration/reset-password.html')