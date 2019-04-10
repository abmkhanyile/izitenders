from django.shortcuts import render

def about_us_view(request):
    return render(request, 'about_us.html')
