from django.db import models

# Create your models here.
class Contact(models.Model):
    phone=models.CharField(max_length=50,unique=True)
    address=models.CharField(max_length=50)

       
    def __str__(self):
        return self.address
    
class Department (models.Model):
    name=models.CharField(max_length=255)
    description=models.TimeField(null=True,blank=True)
    def __str__(self):
        return self.name
class Compensation(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name 
class Employee(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    Contact=models.OneToOneField(Contact,on_delete=models.CASCADE,null=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    comppenstations=models.ManyToManyField(Compensation)
    
    def __str__(self):
        return f'{self.first_name}{self.last_name}'      
    
