from .models import Recipe
from django import forms

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'picture', 'prep_time', 'cook_time', 'servings', 'ingredients', 'directions', ]
        labels = {'cook_time': 'Cook Time'}

