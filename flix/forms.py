from django import forms

from .models import Category, Show

CATEGORY_CHOICES = [(i, i) for i in Category.objects.all()]
print('CATEGORY CHOICES: ', CATEGORY_CHOICES)

class ShowSearchForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'