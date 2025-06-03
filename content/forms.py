from django import forms
from .models import Post
from .models import Comment, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'category', 'tags', 
            'featured_image', 'access_level', 'is_featured', 'is_published'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15}),
            'tags': forms.TextInput(attrs={
                'placeholder': 'Comma-separated tags (e.g., django, python, webdev)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'markdown-editor'})



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }