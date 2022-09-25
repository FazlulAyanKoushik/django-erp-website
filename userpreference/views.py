from locale import currency
from django.contrib import messages
from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference


# Create your views here.

def index(request):
    user_preferences = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':
        currency_data = []
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for k, v in data.items():
                currency_data.append({'name': k, 'value': v})

        context = {
            'currencies': currency_data
        }

        return render(request, 'preferences/index.html', context)

    else:
        currency = request.POST['currency']
        user_preferences.currency = currency
        user_preferences.save()

        messages.success(request, 'chan')
