from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = ['date','description','category','amount']

        widgets = {
            'date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control'}),
        }