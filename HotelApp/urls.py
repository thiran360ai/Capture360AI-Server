from django.urls import path
from .views import *
 

urlpatterns = [
 # customers
   path('create-customer/', create_user_details),
   path('customer-login/', customer_login),
   


   # employees
   
   # path('Employee-login/', Emp_login, name='employee_login'),
   path('create-employee/', create_Employee, name='create_employee'),
   path('employee-login/', Emp_login, name='employee_login'),
   path('total-employees/', total_employees, name='total_employees'),
   path('update-employee/', update_employee, name='update_employee'),
   path('delete-employee/', delete_employee, name='delete_employee'),

]