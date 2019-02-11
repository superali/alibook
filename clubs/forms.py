from django import forms 
from .models import Group
class GroupCreateForm(forms.ModelForm):

    class Meta:
        fields = ('name','content')
        model = Group
    name=forms.CharField(
        label='',
        widget=forms.TextInput(
                    attrs={
            "class":"form-control",
            "ng-model":"page.name",
              "placeholder":'Group Name',

        }
        ),
    ) 
    content=forms.CharField(
        label='',
        widget=forms.Textarea(
                    attrs={
            "class":"form-control",
            "ng-model":"page.content",
               "placeholder":'Group Description',

        }
        ),
    ) 
