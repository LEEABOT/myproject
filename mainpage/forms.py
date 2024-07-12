from django import forms
from .models import Food

class SearchForm(forms.Form):
    query = forms.CharField(label='请输入菜名')

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['foodname', 'foodmaterial', 'foodstep']
