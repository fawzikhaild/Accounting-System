from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.response import Response
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
# from weasyprint import HTML
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from .models import Account, Transaction, Invoice, Payment, Expense, Customer, Vendor
from .forms import AccountForm, TransactionForm, InvoiceForm, PaymentForm, ExpenseForm, CustomerForm, VendorForm,LoginForm
import csv
from openpyxl import Workbook
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from  .decorators import notLoggedUsers,allowedUser,forAdmins


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':            
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                return redirect('home')  
            else:
              
                messages.error(request, 'خطأ في تسجيل الدخول. تأكد من اسم المستخدم أو كلمة المرور.')

       
        return render(request, 'user/login.html')      
    
   

def custom_logout(request):
    logout(request) 
    return redirect('login')
  

@login_required(login_url='login')

@forAdmins
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def account_list(request):
    account_list = Account.objects.all()  
    return render(request, 'accounts/account_list.html', {'accounts': account_list})

def no_permission(request):
    return render(request, 'no_permission.html')
def account_create(request):
    
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            # حفظ البيانات
            form.save()
            messages.success(request, "تم إضافة الحساب بنجاح!")
            return redirect('account_list')  
        else:
            messages.error(request, "يرجى التحقق من المدخلات")
    else:
        form = AccountForm()

    return render(request, 'accounts/account_form.html', {'form': form})

@login_required
def deposit_withdrawal(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    
    if request.method == 'POST':
        transaction_type = request.POST['transaction_type']
        amount = float(request.POST['amount'])
        
        if amount <= 0:
            messages.error(request, "المبلغ يجب أن يكون أكبر من صفر.")
            return redirect('deposit_withdrawal', account_id=account.id)

        try:
            # إنشاء عملية سحب أو إيداع
            transaction = Transaction(
                account=account,
                transaction_type=transaction_type,
                amount=amount,
                user=request.user
            )
            transaction.save()

            messages.success(request, f"تم {transaction_type} بنجاح بمبلغ {amount} ريال.")
            return redirect('account_list')  # إعادة التوجيه إلى قائمة الحسابات بعد العملية
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('deposit_withdrawal', account_id=account.id)

    return render(request, 'accounts/deposit_withdrawal.html', {'account': account})

@login_required
def account_transactions(request, account_id):
    # الحصول على الحساب المحدد
    account = get_object_or_404(Account, id=account_id)

    # الحصول على جميع المعاملات الخاصة بالحساب
    transactions = Transaction.objects.filter(account=account)

    return render(request, 'accounts/account_transactions.html', {'transactions': transactions, 'account': account})
@login_required(login_url='login')
def update_account(request, pk):
    account = get_object_or_404(Account, pk=pk)

    if request.method == 'POST':
        # الحصول على البيانات المدخلة من النموذج
        account.name = request.POST['name']
        account.account_type = request.POST['account_type']
        account.balance = request.POST['balance']
        
        account.save()

        messages.success(request, "تم تحديث الحساب بنجاح!")
        return redirect('account_list')  
    
    return render(request, 'accounts/update_account.html', {'account': account})
@login_required(login_url='login')
def delete_account(request, account_id):
    account = Account.objects.get(id=account_id)
    account.delete()
    return redirect('account_list')

@login_required(login_url='login')
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    return render(request, 'accounts/account_detail.html', {'account': account})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء الحساب بنجاح!")
            return redirect('login')  
        else:
            messages.error(request, "حدث خطأ أثناء إنشاء الحساب.")
    else:
        form = UserCreationForm()

    return render(request, 'user/signup.html', {'form': form})
# عرض المعاملات
@login_required(login_url='login')
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction/transaction_list.html', {'transactions': transactions})
@login_required(login_url='login')
def transaction_create(request):
    accounts = Account.objects.all()  
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()

    return render(request, 'transaction/transaction_form.html', {'form': form, 'accounts': accounts})
@login_required(login_url='login')
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transaction/transaction_form.html', {'form': form, 'transaction': transaction})
@login_required(login_url='login')
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'transaction/transaction_confirm_delete.html', {'transaction': transaction})

# عرض جميع الفواتير
@login_required(login_url='login')
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoice/invoice_list.html', {'invoices': invoices})
@login_required(login_url='login')
def invoice_create(request):
    customers = Customer.objects.all()  
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm() 
    
    return render(request, 'invoice/invoice_form.html', {'form': form, 'customers': customers})
@login_required(login_url='login')
def invoice_detail(request, pk):
    invoice = Invoice.objects.get(id=pk)
    payments = Payment.objects.filter(invoice=invoice)
    return render(request, 'invoice/invoice_detail.html', {'invoice': invoice, 'payments': payments})
@login_required(login_url='login')
def update_invoice(request, invoice_id):
    if request.method == 'POST':
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.status = request.POST.get('status', 'unpaid')
        invoice.save()
        return JsonResponse({'message': 'تم تحديث الفاتورة بنجاح'})
    return JsonResponse({'error': 'حدث خطأ في التحديث'}, status=400)
@login_required(login_url='login')
def invoice_edit(request, pk):
    invoice = Invoice.objects.get(id=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'invoice/invoice_form_update.html', {'form': form})
@login_required(login_url='login')
def invoice_delete(request, pk):
    invoice = Invoice.objects.get(id=pk)
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')
    return render(request, 'invoice/invoice_delete_confirm.html', {'invoice': invoice})

# تقرير الفواتير المتأخرة
@login_required(login_url='login')
def overdue_invoices(request):
    overdue_invoices = Invoice.objects.filter(due_date__lt= datetime.now(), status='unpaid')
    return render(request, 'invoice/overdue_invoices.html', {'invoices': overdue_invoices})
# إضافة دفع
@login_required(login_url='login')
def payment_create(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()
            # Update the invoice status
            invoice.amount_paid += payment.amount
            if invoice.amount_paid >= invoice.amount_due:
                invoice.status = 'paid'
            else:
                invoice.status = 'partial'
            invoice.save()
            return redirect('invoice_list')
    else:
        form = PaymentForm()
    return render(request, 'payment/payment_form.html', {'form': form, 'invoice': invoice})
@login_required(login_url='login')
def payment_list(request):
    
    payments = Payment.objects.all()
    return render(request, 'payment/payment_list.html', {'payments': payments})
@login_required(login_url='login')
def payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'payment/payment_detail.html', {'payment': payment})
@login_required(login_url='login')
def payment_edit(request, payment_id):
   
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        
        if form.is_valid():
            form.save()
            return redirect('payment_list')  
    
    else:
        form = PaymentForm(instance=payment)
 
    return render(request, 'payment/payment_form.html', {'form': form})
@login_required(login_url='login')
def payment_delete(request, payment_id):
  
    payment = get_object_or_404(Payment, id=payment_id)
    
    payment.delete()
    
    return redirect('payment_list')
@login_required(login_url='login')
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expense_form.html', {'form': form})
@login_required(login_url='login')
def expense_list(request):
    expenses = Expense.objects.all()  # جلب جميع النفقات
    return render(request, 'expense_list.html', {'expenses': expenses})
@login_required(login_url='login')
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})
@login_required(login_url='login')
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إضافة العميل بنجاح!")
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'إضافة عميل'})
@login_required(login_url='login')
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})
@login_required(login_url='login')
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل العميل بنجاح!")
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'تعديل العميل'})
@login_required(login_url='login')
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, "تم حذف العميل بنجاح!")
        return redirect('customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})
@login_required(login_url='login')
def export_customers_csv(request):
    customers = Customer.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'الاسم', 'البريد الإلكتروني', 'رقم الهاتف', 'العنوان'])

    for customer in customers:
        writer.writerow([customer.id, customer.name, customer.email, customer.phone, customer.address])

    return response

def export_customers_excel(request):
    customers = Customer.objects.all()

    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="customers.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.append(['ID', 'الاسم', 'البريد الإلكتروني', 'رقم الهاتف', 'العنوان'])

    for customer in customers:
        ws.append([customer.id, customer.name, customer.email, customer.phone, customer.address])

    wb.save(response)
    return response
# عرض الموردين
@login_required(login_url='login')
def vendor_list(request):
    vendors = Vendor.objects.all()  # جلب جميع الموردين
    return render(request, 'vendor/vendor_list.html', {'vendors': vendors})

# إضافة مورد
@login_required(login_url='login')
def vendor_create(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = VendorForm()
    return render(request, 'vendor/vendor_form.html', {'form': form})

# تعديل مورد
@login_required(login_url='login')
def vendor_edit(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendor/vendor_form.html', {'form': form})

# حذف مورد
@login_required(login_url='login')
def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        vendor.delete()
        return redirect('vendor_list')
    return render(request, 'vendor/vendor_delete.html', {'vendor': vendor})
@login_required(login_url='login')
def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    return render(request, 'vendor/vendor_detail.html', {'vendor': vendor})

# تصدير الموردين إلى CSV
def export_vendors_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vendors.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'اسم المورد', 'البريد الإلكتروني', 'رقم الهاتف'])

    vendors = Vendor.objects.all()
    for vendor in vendors:
        writer.writerow([vendor.id, vendor.name, vendor.email, vendor.phone])

    return response

# تصدير الموردين إلى Excel
def export_vendors_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Vendors'

    ws.append(['ID', 'اسم المورد', 'البريد الإلكتروني', 'رقم الهاتف'])

    vendors = Vendor.objects.all()
    for vendor in vendors:
        ws.append([vendor.id, vendor.name, vendor.email, vendor.phone])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="vendors.xlsx"'
    wb.save(response)

    return response


