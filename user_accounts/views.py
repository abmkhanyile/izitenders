from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib import auth
from django.template.context_processors import csrf
from packages.models import Packages
from .forms import (CompanyProfileForm,
                    CustomUserForm,
                    CompanyProfileEditForm,
                    BankingDetailsForm,
                    )
from django.contrib.auth import update_session_auth_hash
from .models import CompanyProfile, OurDetails
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from tender_details.models import Category, Keywords, Province
from django.core import serializers
from django.http import HttpResponse
from django.contrib import messages
import json
import urllib
from django.conf import settings
# from .pdf_render import PDF_Render

def login(request):
    msgStorage = messages.get_messages(request)
    c = {'messages': msgStorage}
    c.update(csrf(request))
    return render(request, 'user_account/login.html', c)

def logout_success_view(request):
    return render(request, 'user_account/logout_success.html')

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/user_account/login')

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/user_account/dashboard')
    else:
        messages.warning(request, "Sorry, that's not a valid username and password")
        return HttpResponseRedirect('/user_account/login')

def subscribe_view(request, billing_cycle, pk):
    packageOption = Packages.objects.get(id=pk)
    if billing_cycle == '1' or billing_cycle == '0':
        b_cycle = billing_cycle
    else:
        b_cycle = '0'

    if request.method == 'POST':                        #checks to see if the request is a POST or GET method
        userRegForm = CustomUserForm(request.POST)      #initilizes the userReg form
        companyForm = CompanyProfileForm(request.POST)  #initilizes the company profile form

        if userRegForm.is_valid() and companyForm.is_valid(): #checks to see if both forms have valid inputs.

            # Begin reCAPTCHA validation
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            # End reCAPTCHA validation

            if result['success']:
                user = userRegForm.save()  # if the userRegForm is valid then it gets saved to the db.
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return render(request, 'user_account/subscribe.html',
                              {'userRegForm': userRegForm, 'package': packageOption, 'billing_cycle': b_cycle,
                               'companyProfileForm': companyForm})


            compProfile = companyForm.save(commit=False)    #if the Company Profile form is valid, we put a hold on saving the form just yet until we can assign a user to it.
            if compProfile.user_id is None:     #if the user is None, then assign it below.
                compProfile.user_id = user.id
                compProfile.accountNumber = 'LH'+str(user.id)
                compProfile.package_id = int(pk)    #assign the package while we are at it.
            compProfile.save()          #save the companyProfile form to the db.

            selected_provinces = companyForm.cleaned_data['provinces'] #extract the selected provinces from the ModelMultiChoiceField.
            selected_cats = companyForm.cleaned_data['tenderCategory']  #extract the selected categories from the ModelMultiChoiceField.
            pymnt_type = companyForm.cleaned_data['pymntMethod']        #get the selected payment type.

            for province_item in selected_provinces:           #Loop through the selected provinces and create a relationship below.
                compProfile.provinces.add(province_item)        #Link the Provinces to their company profile using a ManyToManyField

            for cat_item in selected_cats:
                compProfile.tenderCategory.add(cat_item)

            keyword_ids_str = companyForm.cleaned_data['keywordListItem']
            if keyword_ids_str is not '' or keyword_ids_str is not None:
                keyword_ids = keyword_ids_str.split(',')[:-1]
                for keyword_id in keyword_ids:
                    keywordObj = Keywords.objects.get(id=int(keyword_id.strip()))
                    compProfile.keywords.add(keywordObj)

            if int(pymnt_type) == 2:
                bankingDetails = BankingDetailsForm(request.POST)
                if bankingDetails.is_valid():
                    bankingDetailsObj = bankingDetails.save(commit=False)
                    if bankingDetailsObj.user_CompanyProfile_id is None:
                        bankingDetailsObj.user_CompanyProfile_id = compProfile.user_id
                    bankingDetailsObj.save()

            return HttpResponseRedirect('/user_account/registration_success')
        else:
            bDetailsForm = BankingDetailsForm()
            return render(request, 'user_account/subscribe.html', {'userRegForm': userRegForm, 'package': packageOption, 'billing_cycle': b_cycle, 'companyProfileForm': companyForm, 'bankingDetailsForm': bDetailsForm})
    else:
        userRegForm = CustomUserForm()
        companyProfileForm = CompanyProfileForm()
        bankingDetailsForm = BankingDetailsForm()
        compDetails = OurDetails.objects.all()[0]

        args = {'userRegForm': userRegForm,
                'package': packageOption,
                'billing_cycle': b_cycle,
                'companyProfileForm': companyProfileForm,
                'bankingDetailsForm': bankingDetailsForm,
                'compDetails': compDetails
        }
        args.update(csrf(request))
        return render(request, 'user_account/subscribe.html', args)

def profile_view(request):
    companyProfile = CompanyProfile.objects.get(pk=request.user.id)
    args = {'CompanyProfile': companyProfile}
    return render(request, 'user_account/profile.html', args)


def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/user_account/profile')
        else:
            return redirect('/user_account/password_change')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'pwd_change_form': form}
        return render(request, 'user_account/password_change.html', args)


#Password reset view
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/user_account/profile')
        else:
            return redirect('/user_account/password_change')
    else:
        form = PasswordResetForm(user=request.user)
        args = {'pwd_change_form': form}
        return render(request, 'user_account/password_change.html', args)

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
                if keyword_ids_str is not '' or keyword_ids_str is not None:
                    keyword_ids = keyword_ids_str.split(',')[:-1]
                    editedCompObj.keywords.clear()
                    for keyword_id in keyword_ids:
                        keywordObj = Keywords.objects.get(id=int(keyword_id.strip()))
                        editedCompObj.keywords.add(keywordObj)     #adds keywords to the relationship

            else:
                print('evaluated false...')

            return HttpResponseRedirect('/user_account/profile')
        else:
            companyProfileEditFormObj = CompanyProfileEditForm(instance=compObj)
            return render(request, 'user_account/companyProfileEdit.html', {'compForm': companyProfileEditFormObj, 'compProf': compObj})
    else:
        raise Http404("Company does not exist")


# this handles the pdf render.
# def Invoice_view(request):
#     params = {}
#     # return render(request, 'user_account/invoice.html', params)
#     return PDF_Render.pdfRender('user_account/invoice.html', params)

# this view displays the success page after the user finishes the registration process.
def registration_success_view(request):
    return render(request, 'user_account/registration_success.html')





