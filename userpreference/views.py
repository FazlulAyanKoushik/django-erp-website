from genericpath import exists
from locale import currency
from django.contrib import messages
from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):

    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    # checking User Preference is exit in database?
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
        # user_preferences = None

    context = {
        'currencies': currency_data,
        'user_preferences': user_preferences
    }

    if request.method == 'GET':

        return render(request, 'preferences/index.html', context)

    else:
        currency = request.POST['currency']
        print(f'currency data: {currency}')
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)


        messages.success(request, 'changes saved')
        return render(request, 'preferences/index.html', context)
