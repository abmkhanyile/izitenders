from django import forms
from tender_details.models import Province, Category


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


# the code below, handles to form data for sending the email.
class SendEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control textInput',
        'name': 'email',
        'required': 'required',
        'data-rule-required': 'true',
        'data-msg-required': 'Please enter a valid email address'
    }))

    tender_pk = forms.CharField(widget=forms.HiddenInput(attrs={
        'class': 'tenderPK'
    }))

