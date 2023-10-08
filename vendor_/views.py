from unicodedata import category
from urllib import response

import vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.db import IntegrityError
# from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
# from django.template.defaultfilters import slugify
# from menu.forms import CategoryForm, FoodItemForm
# from menu.models import Category, FoodItem
# from orders.models import Order, OrderedFood

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor

from .forms import VendorForm
from .models import Vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)
