from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room,User
from django.contrib.auth import get_user_model


User = get_user_model()

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #this will create forms from metadata of model like dropdown menu for topic etc.
                           # that is all editabe fields 
        exclude = ['host', 'participants']
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name', 'username', "email", 'bio']
        
        