from django import forms 
from .models import Comment
class PostCreateForm(forms.ModelForm):

    class Meta:
        fields = ('content',)
        model = Post
    content=forms.CharField(
        label='',
        widget=forms.Textarea(
                    attrs={
            "class":"form-control",
 
        }
        ),
    ) 
