from django.shortcuts import render
from packages.models import Packages

def pricing_view(request):
    packages = Packages.objects.all()
    bronze = None
    silver = None
    gold = None
    corporate = None

    for package in packages:
        if package.package_id == 0:
            bronze = package
        elif package.package_id == 1:
            silver = package
        elif package.package_id == 2:
            gold = package
        elif package.package_id == 3:
            corporate = package

    return render(request, 'pricing.html', {'bronze': bronze,
                                            'silver': silver,
                                            'gold': gold,
                                            'corporate': corporate})
