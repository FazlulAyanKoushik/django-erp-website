import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import UserIncome, Source
from userpreference.models import UserPreference


# Create your views here.
@login_required(login_url='/authentication/login')
def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        print('search_str', search_str)
        incomes = UserIncome.objects.filter(
            amount__istartswith = search_str, user = request.user) | UserIncome.objects.filter(
            date__istartswith = search_str, user = request.user) | UserIncome.objects.filter(
            description__icontains = search_str, user = request.user) | UserIncome.objects.filter(
            source__icontains = search_str, user = request.user)       
        data = incomes.values()
        return JsonResponse(list(data), safe=False)
    

@login_required(login_url='/authentication/login')
def index(request):
    item_per_page = 10
    user = User.objects.get(username=request.user)
    income_exist = UserIncome.objects.filter(user=request.user).exists()
    incomes = None
    if income_exist:
        incomes = UserIncome.objects.filter(user=request.user).order_by('-date')
    user_preference_exist  = UserPreference.objects.filter(user=request.user).exists()
    currency = None
    if user_preference_exist:
        currency = UserPreference.objects.get(user=request.user).currency
        
    # pagination
    paginator = Paginator(incomes, item_per_page)
    page_number = request.GET.get('page')
    try:
        incomes_pagination_obj = Paginator.get_page(paginator, page_number)
    except:
        incomes_pagination_obj = {}
    
    if incomes_pagination_obj == {}:
        total_pages = 0
    else:
        total_pages = incomes_pagination_obj.paginator.num_pages

    
    context = {
        'user': user,
        'incomes': incomes_pagination_obj,
        'currency': currency,
        'lastpage': total_pages,
        'total_page_list': [n+1 for n in range(total_pages)]
    }
    return render(request, 'incomes/index.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'form': request.POST
    }
    if request.method == 'GET':
        return render(request, 'incomes/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'incomes/add_income.html', context)
        if not source:
            messages.error(request, 'Source is required')
            return render(request, 'incomes/add_income.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'incomes/add_income.html', context)

        UserIncome.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            source=source,
            date=date
        )
        messages.success(request, 'Record saved successfully')
        return redirect('incomes')

@login_required(login_url='/authentication/login')
def edit_income(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'form': income,  
        'sources': sources,
    }
    if request.method == 'GET':
        return render(request, 'incomes/edit_income.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['source']
        date = request.POST['date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'incomes/edit_income.html', context)
        if not category:
            messages.error(request, 'Category is required')
            return render(request, 'incomes/edit_income.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'incomes/edit_income.html', context)
        
        income.user = request.user
        income.amount = amount
        income.description = description
        income.category = category
        income.date = date
        income.save()
        
        
        messages.success(request, 'Record updated successfully')
        return redirect('incomes')
    

@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('incomes')