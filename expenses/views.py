import json
from urllib import response
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userpreference.models import UserPreference
from .models import Expense, Category
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
import datetime
import random
import csv
import xlwt
from .utils import render_to_pdf
from django.views.generic import View
from django.db.models import Sum

# for genarating pdf invoice
# from io import BytesIO
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# import os

# from django.template.loader import render_to_string
# import tempfile


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

@login_required(login_url='/authentication/login')
def expence_cateogry_summery(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)  
    expenses = Expense.objects.filter(user= request.user, date__gte=six_months_ago, date__lte=todays_date)  
    final_rap = {}
    
    def get_category(expense):
        print(f'Looking for expence : {expense}')
        print(f'Looking for category : {expense.category}')
        return expense.category
    
    category_list = list(set(map(get_category, expenses)))
    print(f'Looking for category : {category_list}')
    
    def get_total_amount_of_expence_by_category(category):
        amount = 0
        filtered_by_category = Expense.objects.filter(user= request.user, category=category)
        
        for item in filtered_by_category:
            amount += item.amount
        
        return amount
          
    for category in category_list:
        final_rap[category] =  get_total_amount_of_expence_by_category(category)
    
    chart_type = random.choice(['bar','pie','doughnut','line','polarArea','radar'])
    
    return JsonResponse({'expence_category_data': final_rap, 'chart_type': chart_type}, safe=False)

def stats(request):
    return render(request, 'expenses/stats.html')


def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expense' + str(datetime.datetime.now()) + '.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])
    
    expenses = Expense.objects.filter(user=request.user)
    
    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])
    
    return response
    
    
def export_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expense' + str(datetime.datetime.now()) + '.xls'
    
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Amount', 'Description', 'Category', 'Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()
    rows = Expense.objects.filter(user=request.user).values_list('amount', 'description', 'category', 'date')
    

    print('Only Objects values are :', rows)
    
    for row in rows:
        row_num+=1
        
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
        
    wb.save(response)
    
    return response 

def export_pdf(request):
    pdf = render_to_pdf("expenses/pdftemplate.html")
    return HttpResponse(pdf, content_type='application/pdf')

class ExportPdfView(View):
    def get(self, request, *args, **kwargs):
        
        expenses = Expense.objects.filter(user=request.user)
        sum = expenses.aggregate(Sum('amount'))
        

        context = {
            'expenses':expenses,
            'total':sum
        }
        pdf = render_to_pdf('expenses/pdf-output.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
    

    
    


        
    
        
    
        
    
    
    
