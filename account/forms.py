# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Account, Transaction, Invoice, Payment, Expense, Customer, Vendor
from django.contrib.auth.forms import AuthenticationForm
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'balance']
        widgets = {
            'balance': forms.NumberInput(attrs={'step': 'any'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'amount', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
       
        fields = ['customer', 'amount_due', 'amount_paid', 'status', 'tax', 'discount', 'currency']
    
  
    amount_due = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    amount_paid = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=[('unpaid', 'غير مدفوعة'), ('paid', 'مدفوعة')], widget=forms.Select(attrs={'class': 'form-control'}))
    tax = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    discount = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    currency = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)


    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

  


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['invoice', 'amount', 'payment_method', 'notes', 'status', 'currency']

    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    payment_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    payment_method = forms.ChoiceField(choices=[('cash', 'نقدي'), ('credit_card', 'بطاقة ائتمان'), ('bank_transfer', 'تحويل بنكي')], widget=forms.Select(attrs={'class': 'form-control'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
    status = forms.ChoiceField(choices=[('paid', 'مدفوع'), ('partial', 'مدفوع جزئيًا'), ('failed', 'فشل الدفع')], widget=forms.Select(attrs={'class': 'form-control'}))
    currency = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'balance', 'address']

    # تخصيص الحقول لإضافة class من خلال widgets
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل الاسم الكامل'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'أدخل البريد الإلكتروني'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل رقم الهاتف'}))
    balance = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'أدخل الرصيد الحالي'}))



class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'email', 'phone']

    # تخصيص الحقول لإضافة class من خلال widgets
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم المورد'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'أدخل البريد الإلكتروني'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل رقم الهاتف'}))

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستخدم'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}))
    
