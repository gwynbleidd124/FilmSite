from django import forms
from django.core.exceptions import ValidationError
from django.forms import Select

from .models import Film, Category, Comments


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')

    class Meta:
        model = Film
        fields = ('title', 'slug', 'content', 'photo', 'rating', 'is_published', 'cat')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'text-input'}),
            'slug': forms.TextInput(attrs={'class': 'text-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'text-input'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'text-input'}),
            'rating': forms.TextInput(attrs={'class': 'text-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }

        labels = {'slug': 'URL'}


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('content', )

        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
