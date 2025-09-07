from django.contrib import admin
from .models import Flat, FlatMember, RentRecord, PaymentRecord

@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    list_display = ['flat_number', 'floor', 'owner', 'monthly_rent', 'total_people', 'created_at']
    list_filter = ['floor', 'owner', 'created_at']
    search_fields = ['flat_number', 'owner__username', 'owner__first_name']
    ordering = ['flat_number']

@admin.register(FlatMember)
class FlatMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'flat', 'phone_number', 'email', 'is_main_renter', 'created_at']
    list_filter = ['flat__owner', 'flat', 'is_main_renter', 'created_at']
    search_fields = ['full_name', 'phone_number', 'email', 'aadhar_number', 'pan_number']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'full_name', 'phone_number', 'email')
        }),
        ('Identity Documents', {
            'fields': ('aadhar_number', 'pan_number', 'aadhar_document', 'pan_document', 'other_documents')
        }),
        ('Flat Information', {
            'fields': ('flat', 'is_main_renter')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(RentRecord)
class RentRecordAdmin(admin.ModelAdmin):
    list_display = ['flat', 'month', 'monthly_rent', 'electricity_bill', 'total_rent', 'total_received', 'remaining_rent', 'payment_status', 'created_at']
    list_filter = ['month', 'flat__owner', 'flat']
    search_fields = ['flat__flat_number', 'flat__owner__username']
    date_hierarchy = 'month'
    readonly_fields = ['electricity_bill', 'total_rent', 'total_received', 'remaining_rent', 'is_fully_paid', 'payment_status']
    
    fieldsets = (
        ('Flat Information', {
            'fields': ('flat', 'month')
        }),
        ('Rent Details', {
            'fields': ('monthly_rent', 'electricity_units', 'electricity_rate')
        }),
        ('Calculated Values', {
            'fields': ('electricity_bill', 'total_rent', 'total_received', 'remaining_rent', 'is_fully_paid', 'payment_status'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def electricity_bill(self, obj):
        return f"₹{obj.electricity_bill}"
    electricity_bill.short_description = 'Electricity Bill'
    
    def total_rent(self, obj):
        return f"₹{obj.total_rent}"
    total_rent.short_description = 'Total Rent'
    
    def total_received(self, obj):
        return f"₹{obj.total_received}"
    total_received.short_description = 'Total Received'
    
    def remaining_rent(self, obj):
        return f"₹{obj.remaining_rent}"
    remaining_rent.short_description = 'Remaining Rent'

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ['rent_record', 'amount_received', 'payment_method', 'payment_by', 'payment_date']
    list_filter = ['payment_method', 'payment_date', 'rent_record__flat__owner', 'rent_record__flat']
    search_fields = ['payment_by', 'rent_record__flat__flat_number', 'notes']
    readonly_fields = ['payment_date']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('rent_record', 'amount_received', 'payment_method', 'payment_by')
        }),
        ('Additional Information', {
            'fields': ('notes', 'payment_date'),
            'classes': ('collapse',)
        })
    )

