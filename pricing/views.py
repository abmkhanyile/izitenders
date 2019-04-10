from django.shortcuts import render
from packages.models import Packages

def pricing_view(request):
    packages = Packages.objects.all()
    return render(request, 'pricing.html', {'packages': packages})
