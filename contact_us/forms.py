from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    surname = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))
    contact_num = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }), required=True)