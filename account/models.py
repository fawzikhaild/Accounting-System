from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
class Account(models.Model):
    ACCOUNT_TYPES = [
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('revenue', 'Revenue'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name



class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'إيداع'),
        ('withdrawal', 'سحب'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES ,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.transaction_type} - {self.amount}'

    def save(self, *args, **kwargs):
        # التأكد من تحويل المبلغ إلى Decimal إذا كان نوعه float
        if isinstance(self.amount, float):
            self.amount = Decimal(str(self.amount))
        
        # عملية الإيداع
        if self.transaction_type == 'deposit':
            self.account.balance += self.amount
        # عملية السحب
        elif self.transaction_type == 'withdrawal':
            if self.account.balance >= self.amount:
                self.account.balance -= self.amount
            else:
                raise ValueError('رصيد الحساب غير كافٍ للسحب')

        # حفظ التعديلات في الحساب
        self.account.save()

        # حفظ المعاملة
        super().save(*args, **kwargs)


class Invoice(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='unpaid')  # Status: unpaid, paid, partial
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Tax for the invoice
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Discount for the invoice
    currency = models.CharField(max_length=10, default='USD')  # Currency for the invoice
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Shipping fee
    notes = models.TextField(blank=True)  # Additional notes for the invoice

    def total_amount(self):
        # حساب المبلغ الإجمالي بعد إضافة الضرائب والخصم
        return self.amount_due + self.tax + self.shipping_fee - self.discount

    def __str__(self):
        return f"Invoice {self.id} for {self.customer.name}"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('bank_transfer', 'Bank Transfer'), ('credit_card', 'Credit Card')],default='cash')
    notes = models.TextField(blank=True)  # Any additional notes about the payment
    status = models.CharField(max_length=10, choices=[('paid', 'مدفوع'), ('partial', 'مدفوع جزئيًا'), ('failed', 'فشل الدفع')], default='paid')
    currency = models.CharField(max_length=10 , default='USD')
    def __str__(self):
        return f"Payment of {self.amount} for Invoice {self.invoice.id} via {self.payment_method}"

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    expense_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Expense of {self.amount} on {self.expense_date}"


# models.py
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # رصيد العميل
    address = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.name



class Vendor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class TransactionEntry(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Transaction {self.transaction.id} - Account: {self.account.name} Debit: {self.debit} Credit: {self.credit}"

class IncomeStatement(models.Model):
    period_start = models.DateField()
    period_end = models.DateField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Income Statement {self.period_start} to {self.period_end}"

class BalanceSheet(models.Model):
    period_start = models.DateField()
    period_end = models.DateField()
    total_assets = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_liabilities = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_equity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Balance Sheet {self.period_start} to {self.period_end}"
