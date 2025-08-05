
from django import forms
from .models import Post, Comment

# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Add a comment...'})
        }

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'placeholder': 'What is on your mind?'}), max_length=1000)

    class Meta:
        model = Post
        fields = ['content', 'image', 'pdf']