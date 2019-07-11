from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib import auth
from django.template.context_processors import csrf
from packages.models import Packages
from .forms import (CustomUserForm,
                    CompanyProfileForm,
                    CompanyProfileEditForm,
                    BankingDetailsForm,
                    PayFast_Form,
                    )
from django.contrib.auth import update_session_auth_hash
from .models import CompanyProfile, OurDetails
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from tender_details.models import Category, Keywords, Province
from django.core import serializers
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
import json
from urllib.parse import urlencode, quote_plus
import hashlib
from django.conf import settings


def login(request):
    msgStorage = messages.get_messages(request)
    c = {'messages': msgStorage}
    c.update(csrf(request))
    return render(request, 'login.html', c)

def logout_success_view(request):
    return render(request, 'user_accounts/logout_success.html')

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/user_accounts/login')

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/user_accounts/dashboard')
    else:
        messages.warning(request, "Sorry, that's not a valid username and password")
        return HttpResponseRedirect('/user_accounts/login')



def register_view(request, billing_cycle, pk):
    packageOption = Packages.objects.get(package_id=pk)
    if billing_cycle == '1' or billing_cycle == '0':
        b_cycle = billing_cycle
    else:
        b_cycle = '0'

    if request.method == 'POST':                        #checks to see if the request is a POST or GET method
        userRegForm = CustomUserForm(request.POST)      #initilizes the userReg form
        companyForm = CompanyProfileForm(request.POST)  #initilizes the company profile form

        if userRegForm.is_valid() and companyForm.is_valid(): #checks to see if both forms have valid inputs.
            user = userRegForm.save()

            compProfile = companyForm.save(commit=False)    #if the Company Profile form is valid, we put a hold on saving the form just yet until we can assign a user to it.
            if compProfile.user_id is None:     #if the user is None, then assign it below.
                compProfile.user_id = user.id
                compProfile.accountNumber = 'TW'+str(user.id)
                compProfile.package_id = packageOption.id    #assign the package while we are at it.
                if b_cycle == '0':
                    compProfile.contractDuration = 6
            compProfile.save()          #save the companyProfile form to the db.

            selected_provinces = companyForm.cleaned_data['provinces'] #extract the selected provinces from the ModelMultiChoiceField.
            selected_cats = companyForm.cleaned_data['tenderCategory']  #extract the selected categories from the ModelMultiChoiceField.
            # pymnt_type = companyForm.cleaned_data['pymntMethod']        #get the selected payment type.

            for province_item in selected_provinces:           #Loop through the selected provinces and create a relationship below.
                compProfile.provinces.add(province_item)        #Link the Provinces to their company profile using a ManyToManyField

            for cat_item in selected_cats:
                compProfile.tenderCategory.add(cat_item)

            return HttpResponseRedirect(reverse('invoice', kwargs={'user_id': user.id, 'comp_prof_id': compProfile.pk}))
        else:
            bDetailsForm = BankingDetailsForm()
            return render(request, 'register.html', {'userRegForm': userRegForm, 'package': packageOption, 'billing_cycle': b_cycle, 'companyProfileForm': companyForm, 'bankingDetailsForm': bDetailsForm})
    else:
        userRegForm = CustomUserForm()
        companyProfileForm = CompanyProfileForm()
        bankingDetailsForm = BankingDetailsForm()
        # compDetails = OurDetails.objects.all()[0]

        args = {'userRegForm': userRegForm,
                'package': packageOption,
                'billing_cycle': b_cycle,
                'companyProfileForm': companyProfileForm,
                'bankingDetailsForm': bankingDetailsForm,
                # 'compDetails': compDetails
        }
        args.update(csrf(request))
        return render(request, 'register.html', args)



def profile_view(request):
    companyProfile = CompanyProfile.objects.get(pk=request.user.id)
    args = {'CompanyProfile': companyProfile}
    return render(request, 'profile.html', args)


def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/user_accounts/profile')
        else:
            return redirect('/user_accounts/password_change')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'pwd_change_form': form}
        return render(request, 'user_accounts/password_change.html', args)


#Password reset view
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/user_accounts/profile')
        else:
            return redirect('/user_accounts/password_change')
    else:
        form = PasswordResetForm(user=request.user)
        args = {'pwd_change_form': form}
        return render(request, 'user_accounts/password_change.html', args)

#This is the function that handle the auto complete search functionality.
def autocomplete_search_view(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
        return HttpResponse([{}], content_type='application/json')

    swList = search_text.split()

    keywords = []
    if len(swList) == 1:
        keywords = Keywords.objects.filter(keyword__icontains=swList[0].strip())
    else:
        keywords = Keywords.objects.filter(keyword__icontains=swList[0].strip()).filter(keyword__icontains=swList[1].strip())

    data = serializers.serialize('json', keywords, fields=('keyword'))
    return HttpResponse(data, content_type='application/json')


# this view handles the update of the Company Profile.
def UpdateCompanyProfile(request, pk):
    compObj = get_object_or_404(CompanyProfile, pk=pk)

    if request.user == compObj.user:
        if request.method == 'POST':
            companyProfileEditFormObj = CompanyProfileEditForm(data=request.POST, instance=compObj)
            if companyProfileEditFormObj.is_valid():
                editedCompObj = companyProfileEditFormObj.save()

                keyword_ids_str = companyProfileEditFormObj.cleaned_data['keywordListItem']

                if len(keyword_ids_str) > 0:
                    keyword_ids = keyword_ids_str.split(',')
                    editedCompObj.keywords.clear()
                    for keyword_id in keyword_ids:
                        keywordObj = Keywords.objects.get(id=int(keyword_id.strip()))
                        editedCompObj.keywords.add(keywordObj)     #adds keywords to the relationship

            else:
                print('evaluated false...')

            return HttpResponseRedirect('/user_accounts/profile')
        else:
            companyProfileEditFormObj = CompanyProfileEditForm(instance=compObj)
            return render(request, 'companyProfileEdit.html', {'compForm': companyProfileEditFormObj, 'compProf': compObj})
    else:
        raise Http404("Company does not exist")


# this view displays the success page after the user finishes the registration process.
def registration_success_view(request):
    return render(request, 'registration_success.html')

def Payment_Success_View(request):
    return render(request, 'payment_success.html')

def Payment_Cancelled_View(request):
    return render(request, 'payment_cancelled.html')


# this handles the pdf render.
def Invoice_view(request, user_id, comp_prof_id):
    userObj = User.objects.get(id=user_id)
    compProfile = CompanyProfile.objects.get(pk=comp_prof_id)
    ourDetails = OurDetails.objects.get(compName='TenderWiz')

    amount = None

    if compProfile.contractDuration == 6:
        amount = compProfile.package.sixMonthPrice
    else:
        amount = compProfile.package.annualPrice

    payfast_data = {
        'merchant_id': '10012886',
        'merchant_key': 'sb5koxsz8qp59',
        'return_url': 'https://tenderwiz.herokuapp.com/user_accounts/payment_success/',
        'cancel_url': 'https://tenderwiz.herokuapp.com/user_accounts/payment_cancelled/',
        'name_first': userObj.first_name,
        'name_last': userObj.last_name,
        'email_address': userObj.email,
        'cell_number': compProfile.contactNumber,
        'm_payment_id': '01AB',
        'amount': amount,
        'item_name': compProfile.package.package,
        'email_confirmation': '1',
        'confirmation_address': ourDetails.emailAddress
    }

    signature = ''
    # for key, value in payfast_data.items():
    #     signature += '{}={}&'.format(str(key), str(urllib.parse.urlencode(value)))

    signature = urlencode(payfast_data, quote_via=quote_plus)


    print(signature)

    signature = hashlib.md5(signature.encode()).hexdigest()

    print(signature)
    payfast_data.update({'signature': signature})

    payfastForm = PayFast_Form(payfast_data)

    return render(request, 'invoice.html', {'user': userObj,
                                            'comp_prof': compProfile,
                                            'ourDetails': ourDetails,
                                            'payfast_form': payfastForm,
                                            'signature': signature.strip()})












