from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from . models import *
from . forms import *
from django.urls import reverse_lazy


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact_form.html'
    success_url = reverse_lazy('contact-create')

class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department_form.html'
    success_url = reverse_lazy('department-create')

class CompensationCreateView(CreateView):
    model = Compensation
    form_class = CompensationForm
    template_name = 'compensation_form.html'
    success_url = reverse_lazy('compensation-create')

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('employee-create')
