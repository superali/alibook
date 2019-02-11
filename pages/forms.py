from django import forms 
from .models import Page
class PageCreateForm(forms.ModelForm):

    class Meta:
        fields = ('name','content')
        model = Page

    name=forms.CharField(
        label='',
        widget=forms.TextInput(
                    attrs={
            "class":"form-control",
            "ng-model":"page.name",
              "placeholder":'Page Name',

        }
        ),
    ) 
    content=forms.CharField(
        label='',
        widget=forms.Textarea(
                    attrs={
            "class":"form-control",
            "ng-model":"page.content",
               "placeholder":'Page Description',

        }
        ),
    ) 
