from django import forms
from .models import Testimonials
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



#handles the testimonials on the homepage
class TestimonialsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'textInput field-long',
        'name': 'fname field1',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'textInput field-long',
        'name': 'lname field1',
        'placeholder': 'Last name'
    }))

    designation = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'textInput field-long',
        'name': 'designation field1',
        'placeholder': 'Designation'
    }))
    company_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'textInput field-long',
        'name': 'comp_name field1',
        'placeholder': 'Company name'
    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'field-textarea field-long',
        'name': 'message'
    }))

    class Meta:
        model = Testimonials
        fields = (
            'first_name',
            'last_name',
            'designation',
            'company_name',
            'message',
        )