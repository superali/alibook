from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm ,UserChangeForm
from django import forms 
User =get_user_model()

class UserLoginForm(forms.Form):

    username=forms.CharField(
       label='',
        widget=forms.TextInput(
        attrs={
            "class":"form-control",
             "placeholder":_("username"),
             "id":'username',
             "ng-model":'user.username'

        }
        ))
    
    password=forms.CharField(
       label='',
        widget=forms.PasswordInput(
        attrs={
            "class":"form-control",
            "placeholder":_("password"),
             "id":'password',
             "ng-model":'user.password'


        }
        ))

    
class UserSignUpForm(UserCreationForm):
    class Meta:
        fields = ('username','email','password1','password2')
        model = User
    username=forms.CharField(
        help_text=_( 'username cant contain spaces'),
        label='',
        widget=forms.TextInput(
        attrs={
            "class":"form-control",
            "placeholder":_("username"),
             "ng-model":'signup.username',

        }
        ))
    
    email=forms.EmailField(
       label='',
        widget=forms.TextInput(
        attrs={
            "class":"form-control",
            "placeholder":_("Email"),
             "ng-model":'signup.email',

        }
        ))
    

    password1=forms.CharField(
           label='',
            widget=forms.PasswordInput(
            attrs={
                "class":"form-control",
         "placeholder":_("password"),
             "ng-model":'signup.password1',

            }
            ))
    password2=forms.CharField(
           label='',
            widget=forms.PasswordInput(
            attrs={
                "class":"form-control",
                 "placeholder":_("confirm password"),
             "ng-model":'signup.password2',

            }
            ))
    


