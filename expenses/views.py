from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userpreference.models import UserPreference
from .models import Expense, Category


# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(user=request.user)
    user_preference = UserPreference.objects.get(user=request.user)
    context = {
        'expenses': expenses,
        'user_preference': user_preference
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
