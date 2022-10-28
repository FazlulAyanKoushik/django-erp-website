import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userpreference.models import UserPreference
from .models import Expense, Category
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse


# Create your views here.
@login_required(login_url='/authentication/login')
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        print('search_str', search_str)
        expenses = Expense.objects.filter(
            amount__istartswith = search_str, user = request.user) | Expense.objects.filter(
            date__istartswith = search_str, user = request.user) | Expense.objects.filter(
            description__icontains = search_str, user = request.user) | Expense.objects.filter(
            category__icontains = search_str, user = request.user)       
        data = expenses.values()
        return JsonResponse(list(data), safe=False)

            
@login_required(login_url='/authentication/login')
def index(request):
    item_per_page = 10
    user = User.objects.get(username=request.user)
    expense_exist = Expense.objects.filter(user=request.user).exists()
    expenses = None
    if expense_exist:
        expenses = Expense.objects.filter(user=request.user).order_by('-date')
    user_preference_exist  = UserPreference.objects.filter(user=request.user).exists()
    currency = None
    if user_preference_exist:
        currency = UserPreference.objects.get(user=request.user).currency
        
    # pagination
    paginator = Paginator(expenses, item_per_page)
    page_number = request.GET.get('page')
    try:
        expenses_pagination_obj = paginator.get_page(page_number)
    except:
        expenses_pagination_obj = {}
    if expenses_pagination_obj == {}:
        total_pages = 0
    else:
        total_pages = expenses_pagination_obj.paginator.num_pages
    
    context = {
        'user': user,
        'expenses': expenses_pagination_obj,
        'currency': currency,
        'lastpage': total_pages,
        'total_page_list': [n+1 for n in range(total_pages)]
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'form': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        if not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/add_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            category=category,
            date=date
        )
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')

@login_required(login_url='/authentication/login')
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'form': expense,  
        'categories': categories,
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html', context)
        if not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/edit_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/edit_expense.html', context)
        
        expense.user = request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()
        
        
        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')

@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted successfully')
    return redirect('expenses')


        
    
        
    
        
    
    
    
