from django import forms 
from .models import Message
class MessageCreateForm(forms.ModelForm):

    class Meta:
        fields = ('content',)
        model = Message
    content=forms.CharField(
        required=False,
        label='',
        widget=forms.Textarea(
                    attrs={
            "id":"msgContent",
            "class":"form-control",
            "ng-model":"message.content",
 
        }
        ),
    ) 
