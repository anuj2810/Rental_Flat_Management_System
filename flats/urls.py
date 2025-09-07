from django.urls import path
from . import views

app_name = 'flats'

urlpatterns = [
    path('add/', views.add_flat, name='add_flat'),
    # flats_list URL removed
    path('manage/', views.manage_flats, name='manage_flats'),
    path('member/<int:member_id>/view/', views.view_member_detail, name='view_member_detail'),
    path('member/<int:member_id>/update/', views.update_member_detail, name='update_member_detail'),
    path('<int:flat_id>/', views.flat_detail, name='flat_detail'),
    path('<int:flat_id>/add-member/', views.add_flat_member, name='add_flat_member'),
    path('<int:flat_id>/manage-rent/', views.manage_rent, name='manage_rent'),
    path('<int:flat_id>/payment-records/', views.flat_payment_records, name='flat_payment_records'),
    path('edit-rent/<int:record_id>/', views.edit_rent, name='edit_rent'),
    path('delete-rent/<int:record_id>/', views.delete_rent, name='delete_rent'),
    path('add-payment/<int:record_id>/', views.add_payment, name='add_payment'),
    path('edit-payment/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('delete-payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('payment-history/<int:record_id>/', views.payment_history, name='payment_history'),
    path('bulk-delete-payments/<int:record_id>/', views.bulk_delete_payments, name='bulk_delete_payments'),
    path('payment-summary/', views.payment_summary, name='payment_summary'),
    path('comprehensive-payment-summary/', views.comprehensive_payment_summary, name='comprehensive_payment_summary'),
    path('delete-flat/<int:flat_id>/', views.delete_flat, name='delete_flat'),
]