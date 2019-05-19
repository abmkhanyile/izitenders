from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CompanyProfile, Banking_Details
from tender_details.models import Province, Category, Keywords


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'textInput field-divided',
        'id': 'firstname-99a6d115-5e68-4355-a7d0-529207feb0b3_2983',
        'name': 'firstname field1',
        'required': 'required',
        'data-rule-required': 'true',
        'data-msg-required': 'Please enter your first name',
        'placeholder': 'Firstname'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'textInput field-divided',
        'id': 'lastname-99a6d115-5e68-4355-a7d0-529207feb0b3_2983',
        'name': 'lastname field2',
        'required': 'required',
        'data-rule-required': 'true',
        'data-msg-required': 'Please enter your last name',
        'placeholder': 'Lastname'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'textInput field-long',
        'id': 'email-99a6d115-5e68-4355-a7d0-529207feb0b3_2983',
        'name': 'email field3',
        'required': 'required',
        'data-rule-required': 'true',
        'data-msg-required': 'Please enter a valid email address'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'textInput field-divided',
        'id': 'password1-99a6d115-5e68-4355-a7d0-529207feb0b3_2983',
        'name': 'password1 field1',
        'required': 'required',
        'data-rule-required': 'true',
        'data-msg-required': 'Please enter password 1',
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'field-divided',
        'id': 'password2-99a6d115-5e68-4355-a7d0-529207feb0b3_2983',
        'name': 'password2 field2',
        'required': 'required',
        'data-rule-required': 'true',
        'data-msg-required': 'Please enter password 2',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'class': 'textInput field-long',
                                               'name': 'username',
                                               'placeholder': 'Username'
                                               }),
        }
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",
                  )

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class CompanyProfileForm(ModelForm):
    provinces = forms.ModelMultipleChoiceField(queryset=Province.objects.all(), widget=forms.SelectMultiple(attrs={
        'id': 'provinces'
    }))

    tenderCategory = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.SelectMultiple(attrs={
        'id': 'catSelect'
    }))

    # keywordListItem = forms.CharField(widget=forms.HiddenInput(attrs={
    #     'class': 'keywordListItem'
    # }))

    class Meta:
        model = CompanyProfile
        exclude = (
            'user',
            'keywords',
            'accountNumber',
            'commencementDate',
            'package',
            'contractDuration',
        )
        fields = (
            'companyName',
            'companyRegNum',
            'contactNumber',
            'address',
            'areaCode',
            'deliveryEmails',
            'provinces',
            'tenderCategory',
            'pymntMethod',
            'termsAndConditions',
        )

        widgets = {
            'companyName': forms.TextInput(attrs={
                'class': 'field-long',
                'id': 'companyNameId',
                'name': 'companyName',
                'required': 'required',
                'data-rule-required': 'true',
                'data-msg-required': 'Please enter company name'
            }),
            'companyRegNum': forms.TextInput(attrs={
                'class': 'field-long',
                'id': 'companyRegNumId',
                'name': 'companyRegNum',
                'required': 'required',
                'data-rule-required': 'true',
                'data-msg-required': 'Please enter company reg number'
            }),
            'contactNumber': forms.TextInput(attrs={
                'class': 'field-long input_field',
                'id': 'contactNum',
                'name': 'contactNumber',
                'required': 'required',
                'data-rule-required': 'true',
                'data-msg-required': 'Please enter contact number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'field-textarea field-long',
                'id': 'addressId',
                'name': 'address',
                'required': 'required',
                'data-rule-required': 'true',
                'data-msg-required': 'Please enter the address'
            }),
            'areaCode': forms.TextInput(attrs={
                'class': 'field-long',
                'id': 'areaCodeId',
                'name': 'areaCode',
                'required': 'required',
                'data-rule-required': 'true',
                'data-msg-required': 'Please enter the areaCode'
            }),
            'deliveryEmails': forms.TextInput(attrs={
                'class': 'field-long textInput',
                'id': 'deliveryEmailId',
                'name': 'deliveryEmails',
                'required': 'required',
                'data-rule-required': 'true',
                'data-msg-required': 'Please enter the email address(s)'
            }),


            'package': forms.HiddenInput(),
            'pymntMethod': forms.HiddenInput(attrs={
                'id': 'pymntType'
            }),
            'termsAndConditions': forms.CheckboxInput(attrs={
                'id': 'termsAndConditions'
            })
        }


# class below handles the profile editing by the user.
class CompanyProfileEditForm(ModelForm):
    keywordListItem = forms.CharField(required=False, widget=forms.HiddenInput(attrs={
        'class': 'keywordListItem'
    }))

    class Meta:
        model = CompanyProfile
        exclude = (
            'user',
            'accountNumber',
            'keywords',
            'commencementDate',
            'package',
            'deliveryEmails',
            'contractDuration',
        )
        fields = (
            'contactNumber',
            'address',
            'areaCode',
            'keywordListItem',
        )

        widgets = {
            'contactNumber': forms.TextInput(attrs={
                'class': 'form-control input_field',
                'id': 'contactNum',
                'name': 'contactNumber',
                'required': 'required',
                'data-rule-required': 'true',
                'data-msg-required': 'Please enter contact number'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'addressId',
                'name': 'address',
                'required': 'required',
                'data-rule-required': 'true',
                'data-msg-required': 'Please enter the address'
            }),
            'areaCode': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'areaCodeId',
                'name': 'areaCode',
                'required': 'required',
                'data-rule-required': 'true',
                'data-msg-required': 'Please enter the areaCode'
            }),
            'deliveryEmails': forms.TextInput(attrs={
                'class': 'form-control textInput',
                'id': 'deliveryEmailId',
                'name': 'deliveryEmails',
                'required': 'required',
                'data-rule-required': 'true',
                'data-msg-required': 'Please enter the email address(s)'
            }),
        }


# this is the banking details form below.
class BankingDetailsForm(ModelForm):
    class Meta:
        model = Banking_Details
        exclude = (
            'user_CompanyProfile',
        )
        fields = (
            'accHolder',
            'bankName',
            'accNum',
            'accType',
            'branchName',
            'branchCode',
        )
        widgets = {
            'accHolder': forms.TextInput(attrs={
                'class': 'form-control m-1 bdfield',
                'type': 'text',
                'placeholder': 'Account Holder',
                'disabled': 'disabled'
            }),
            'bankName': forms.TextInput(attrs={
                'class': 'form-control m-1 bdfield',
                'type': 'text',
                'placeholder': 'Bank Name',
                'disabled': 'disabled'
            }),
            'accNum': forms.TextInput(attrs={
                'class': 'form-control m-1 bdfield',
                'type': 'text',
                'placeholder': 'Account Number',
                'disabled': 'disabled'
            }),
            'accType': forms.Select(attrs={
                'class': 'form-control m-1 bdfield',
                'disabled': 'disabled'
            }),
            'branchName': forms.TextInput(attrs={
                'class': 'form-control m-1 bdfield',
                'type': 'text',
                'placeholder': 'Branch',
                'disabled': 'disabled'
            }),
            'branchCode': forms.TextInput(attrs={
                'class': 'form-control m-1 bdfield',
                'type': 'text',
                'placeholder': 'Branch Code',
                'disabled': 'disabled'
            })
        }


