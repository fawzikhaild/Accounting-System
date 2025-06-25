from django.urls import path
from . views import *
urlpatterns = [
    path('', ContactCreateView.as_view(), name='contact-create'),
    path('department/create/', DepartmentCreateView.as_view(), name='department-create'),
    path('compensation/create/', CompensationCreateView.as_view(), name='compensation-create'),
    path('employee/create/', EmployeeCreateView.as_view(), name='employee-create'),
]
