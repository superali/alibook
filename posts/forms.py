from django import forms 
from .models import Post
class PostCreateForm(forms.ModelForm):

    class Meta:
        fields = ('content',)
        model = Post
    content=forms.CharField(
        required=False,
        label='',
        widget=forms.Textarea(
                    attrs={
            "class":"form-control",
            "ng-model":"post.content",
 
        }
        ),
    ) 
