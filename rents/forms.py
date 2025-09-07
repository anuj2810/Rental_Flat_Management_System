from django import forms
from .models import RentRecord
from flats.models import FlatMember

class RentRecordForm(forms.ModelForm):
    payment_made_by = forms.ChoiceField(
        choices=[], 
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    
    class Meta:
        model = RentRecord
        fields = [
            'month', 'monthly_rent', 'electricity_units', 'electricity_rate',
            'rent_received', 'payment_date', 'payment_made_by'
        ]
        widgets = {
            'month': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
            'monthly_rent': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.01'
            }),
            'electricity_units': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.01'
            }),
            'electricity_rate': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.01'
            }),
            'rent_received': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.01'
            }),
            'payment_date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        renter_id = kwargs.pop('renter_id', None)
        super().__init__(*args, **kwargs)
        
        if renter_id:
            try:
                renter = FlatMember.objects.get(id=renter_id)
                # Get all flat members for this flat
                flat_members = FlatMember.objects.filter(flat=renter.flat)
                
                # Create choices for payment_made_by dropdown
                choices = [('', 'Select who made the payment')]
                
                for member in flat_members:
                    member_type = "(Main Renter)" if member.is_main_renter else "(Member)"
                    choices.append((member.full_name, f"{member.full_name} {member_type}"))
                
                self.fields['payment_made_by'].choices = choices
            except FlatMember.DoesNotExist:
                pass