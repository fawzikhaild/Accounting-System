from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # الصفحة الرئيسية
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
     path('logout/', views.custom_logout, name='logout'),
     path('signup/', views.signup_view, name='signup'),
      path('no_permission/', views.no_permission, name='no_permission'),
    # path('login/', views.LoginView.as_view(), name='login'),
    #  path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # المسار لتسجيل الدخول
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # عرض الحسابات
    path('accounts/', views.account_list, name='account_list'), 
    path('account/create/', views.account_create, name='account_create'),  
        path('accounts/<int:pk>/update/', views.update_account, name='update_account'),
    path('accounts/<int:account_id>/delete/', views.delete_account, name='delete_account'),
    path('accounts/<int:account_id>/detail/', views.account_detail, name='account_detail'),
     path('account/deposit_withdrawal/<int:account_id>/', views.deposit_withdrawal, name='deposit_withdrawal'),
      path('account/transactions/<int:account_id>/', views.account_transactions, name='account_transactions'),
    # المعاملات
    path('transactions/', views.transaction_list, name='transaction_list'),  
    path('transaction/create/', views.transaction_create, name='transaction_create'),  
    path('transaction/edit/<int:pk>/', views.transaction_edit, name='transaction_edit'),  
    path('transaction/delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),  

    # الفواتير
    path('invoices/', views.invoice_list, name='invoice_list'),  
    path('invoice/create/', views.invoice_create, name='invoice_create'),  
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),  
    path('invoice/edit/<int:pk>/', views.invoice_edit, name='invoice_edit'),  
    path('invoice/delete/<int:pk>/', views.invoice_delete, name='invoice_delete'),  
    path('invoices/overdue/', views.overdue_invoices, name='overdue_invoices'), 
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    # path('invoice/<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    # المدفوعات
     path('payment/', views.payment_list, name='payment_list'),
    path('payment/create/<int:invoice_id>/', views.payment_create, name='payment_create'),  
     path('payment/<int:payment_id>/', views.payment_detail, name='payment_detail'), 
    path('payment/<int:payment_id>/edit/', views.payment_edit, name='payment_edit'),  
    path('payment/<int:payment_id>/delete/', views.payment_delete, name='payment_delete'),  
    # النفقات
    path('expenses/create/', views.expense_create, name='expense_create'),  
     path('expenses/', views.expense_list, name='expense_list'), 
    # العملاء
     path('customers/', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customer/create/', views.customer_create, name='customer_create'),
    path('customer/edit/<int:pk>/', views.customer_edit, name='customer_edit'),
    path('customer/delete/<int:pk>/', views.customer_delete, name='customer_delete'),
     path('customers/export/csv/', views.export_customers_csv, name='export_customers_csv'),
    path('customers/export/excel/', views.export_customers_excel, name='export_customers_excel'),
    # الموردين
   path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/create/', views.vendor_create, name='vendor_create'),
    path('vendors/edit/<int:pk>/', views.vendor_edit, name='vendor_edit'),
    path('vendors/detail/<int:pk>/', views.vendor_detail, name='vendor_detail'),  
    path('vendors/delete/<int:pk>/', views.vendor_delete, name='vendor_delete'),  
    path('vendors/export/csv/', views.export_vendors_csv, name='export_vendors_csv'),
    path('vendors/export/excel/', views.export_vendors_excel, name='export_vendors_excel'),
    
]
