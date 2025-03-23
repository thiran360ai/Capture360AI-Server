from django.contrib.auth.backends import BaseBackend
from .models import Employee

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Employee.objects.get(email=email)
            if user.check_password(password):
                return user
        except Employee.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Employee.objects.get(pk=user_id)
        except Employee.DoesNotExist:
            return None
