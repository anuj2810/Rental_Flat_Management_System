from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from .forms import CustomUserCreationForm, LoginForm, ProfileForm
from .models import CustomUser
from flats.models import FlatMember, Flat, RentRecord, PaymentRecord

def homepage_view(request):
    """Homepage view with project information and statistics"""
    # Get some statistics for the homepage
    total_properties = Flat.objects.count()
    total_tenants = FlatMember.objects.count()
    total_rent_records = RentRecord.objects.count()
    total_payments = PaymentRecord.objects.count()

    # Calculate total rent collected
    total_rent_collected = sum(payment.amount_received for payment in PaymentRecord.objects.all())

    context = {
        'total_properties': total_properties,
        'total_tenants': total_tenants,
        'total_rent_records': total_rent_records,
        'total_payments': total_payments,
        'total_rent_collected': total_rent_collected,
    }

    return render(request, 'accounts/homepage.html', context)

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.user.user_type == 'owner':
        # Only show renters for flats owned by the current owner
        renters = FlatMember.objects.filter(flat__owner=request.user)
        # Get the actual flats count for the current owner
        from flats.models import Flat
        total_flats = Flat.objects.filter(owner=request.user).count()
        return render(request, 'accounts/owner_dashboard.html', {
            'renters': renters,
            'total_flats': total_flats
        })
    else:
        try:
            renter_profile = FlatMember.objects.get(user=request.user)
            return render(request, 'accounts/renter_dashboard.html', {'renter': renter_profile})
        except FlatMember.DoesNotExist:
            messages.error(request, 'Renter profile not found. Please contact the owner.')
            return render(request, 'accounts/renter_dashboard.html', {'renter': None})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


def media_debug_view(request):
    """Debug view to check media file serving"""
    from django.conf import settings
    import os

    media_info = {
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_ROOT': str(settings.MEDIA_ROOT),
        'media_root_exists': os.path.exists(settings.MEDIA_ROOT),
        'profiles_dir_exists': os.path.exists(os.path.join(settings.MEDIA_ROOT, 'profiles')),
        'debug_mode': settings.DEBUG,
    }

    # List files in media directory
    if os.path.exists(settings.MEDIA_ROOT):
        media_files = []
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), settings.MEDIA_ROOT)
                media_files.append(rel_path)
        media_info['media_files'] = media_files

    return JsonResponse(media_info)