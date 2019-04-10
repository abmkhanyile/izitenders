from django import forms
from tender_details.models import Category, Province

class TenderSearchForm(forms.Form):
    searchField = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'id': 'searchField_id',
        'class': 'form-control w-100',
        'placeholder': 'Search for tenders'
    }))
    categorySelectionField = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                            widget=forms.SelectMultiple(attrs={
                                                                'id': 'searchCategory',
                                                            }))
    provinceSelectionField = forms.ModelMultipleChoiceField(queryset=Province.objects.all(), widget=forms.SelectMultiple(attrs={
        'id': 'searchRegion',
    }))