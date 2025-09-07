from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'rents'

urlpatterns = [
    # Redirect old rent URLs to new flat-based URLs
    path('manage/<int:renter_id>/', lambda request, renter_id: redirect('flats:manage_rent', flat_id=renter_id), name='manage_rent'),
    path('edit/<int:record_id>/', lambda request, record_id: redirect('flats:edit_rent', record_id=record_id), name='edit_rent'),
    path('payment-summary/', lambda request: redirect('flats:payment_summary'), name='payment_summary'),
    path('my-history/', views.renter_rent_history, name='renter_rent_history'),
]