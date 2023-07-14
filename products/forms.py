from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {'body': False}
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'cols': '30',
                    'rows': '7',
                    'class': 'form-control',
                    'placeholder': 'Comment'
                }
            )
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {'body': False}
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'cols': '30',
                    'rows': '7',
                    'class': 'form-control',
                    'placeholder': 'Comment'
                }
            )
        }
