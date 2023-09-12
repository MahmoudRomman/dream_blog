from django import forms
from . import models


class PostForm(forms.ModelForm):
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={
        'class' : 'ckeditor',
        'required' : False,
        'cols' : 30,
        'rows' : 10,
    }))


    class Meta:
        model = models.Post
        fields = ('title', 'overview', 'content', 'thumbnail', 'categories', 'featured')




class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : "Type your comment...",
        'id' : 'UserComment', 
        'rows' : '4',
    }))

    class Meta:
        model = models.Comment
        fields = ('content',)