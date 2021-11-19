from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import *

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UpdateUserForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'phone', 'email']
