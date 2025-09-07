from django import forms
from .models import Flat, FlatMember, RentRecord, PaymentRecord
from accounts.models import CustomUser

class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = ['flat_number', 'floor', 'monthly_rent']
        widgets = {
            'flat_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter flat number (e.g., 101, A-1)'
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter floor number'
            }),
            'monthly_rent': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.01',
                'placeholder': 'Monthly rent amount'
            })
        }

class FlatMemberForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    is_main_renter = forms.BooleanField(required=False, initial=False, help_text="Main renter who will have login access")
    
    class Meta:
        model = FlatMember
        fields = [
            'full_name', 'phone_number', 'email', 'aadhar_number', 
            'pan_number', 'aadhar_document', 'pan_document', 'other_documents', 'notes'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'aadhar_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'maxlength': '12'}),
            'pan_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'maxlength': '10'}),
            'aadhar_document': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'pan_document': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'other_documents': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.flat = kwargs.pop('flat', None)
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            if field_name not in ['username', 'password', 'is_main_renter']:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
                })
        
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Username for main renter login (optional)'
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Password for main renter login (optional)'
        })
        
        self.fields['is_main_renter'].widget.attrs.update({
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
        })
    
    def clean(self):
        cleaned_data = super().clean()
        is_main_renter = cleaned_data.get('is_main_renter')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if is_main_renter and (not username or not password):
            raise forms.ValidationError("Username and password are required for main renter.")
        
        # Check if there's already a main renter for this flat
        if is_main_renter and self.flat:
            existing_main = FlatMember.objects.filter(flat=self.flat, is_main_renter=True).exclude(pk=self.instance.pk if self.instance.pk else None)
            if existing_main.exists():
                raise forms.ValidationError("This flat already has a main renter.")
        
        return cleaned_data
    
    def save(self, commit=True):
        # Create user account only if it's a main renter
        user = None
        if self.cleaned_data.get('is_main_renter') and self.cleaned_data.get('username'):
            user = CustomUser.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['full_name'].split()[0],
                last_name=' '.join(self.cleaned_data['full_name'].split()[1:]) if len(self.cleaned_data['full_name'].split()) > 1 else '',
                user_type='renter'
            )
        
        # Create the flat member
        flat_member = super().save(commit=False)
        flat_member.flat = self.flat
        flat_member.user = user
        flat_member.is_main_renter = self.cleaned_data.get('is_main_renter', False)
        if commit:
            flat_member.save()
        return flat_member

class RentRecordForm(forms.ModelForm):
    class Meta:
        model = RentRecord
        fields = [
            'month', 'monthly_rent', 'electricity_units', 'electricity_rate'
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
        }
    
    def __init__(self, *args, **kwargs):
        flat_id = kwargs.pop('flat_id', None)
        super().__init__(*args, **kwargs)
        
        if flat_id:
            try:
                flat = Flat.objects.get(id=flat_id)
                # Set default monthly rent from flat
                if not self.instance.pk:  # Only for new records
                    self.fields['monthly_rent'].initial = flat.monthly_rent
            except Flat.DoesNotExist:
                pass

class PaymentRecordForm(forms.ModelForm):
    payment_by = forms.ChoiceField(
        choices=[],  # Will be populated in __init__
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        required=True,
        label="Payment Made By"
    )
    
    class Meta:
        model = PaymentRecord
        fields = [
            'amount_received', 'payment_method', 'payment_by', 'notes'
        ]
        widgets = {
            'amount_received': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.01',
                'placeholder': 'Enter amount received'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': '3',
                'placeholder': 'Additional notes (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.rent_record = kwargs.pop('rent_record', None)
        super().__init__(*args, **kwargs)
        
        if self.rent_record:
            try:
                # Set max amount to remaining rent
                remaining = self.rent_record.remaining_rent
                self.fields['amount_received'].widget.attrs['max'] = str(remaining)
                self.fields['amount_received'].help_text = f"Maximum amount: ₹{remaining}"
                
                # Populate payment_by dropdown with flat members
                flat_members = self.rent_record.flat.flat_members.all()
                choices = [('', 'Select who made the payment')]
                for member in flat_members:
                    choices.append((member.full_name, member.full_name))
                
                # Update the choices for the payment_by field
                self.fields['payment_by'].choices = choices
                
                # Set initial value to first member if available
                if flat_members.exists() and not self.instance.pk:
                    self.fields['payment_by'].initial = flat_members.first().full_name
            except Exception as e:
                # If there's an error calculating remaining rent, set a default
                self.fields['amount_received'].help_text = "Enter the amount received"
                # Set default choices for payment_by
                self.fields['payment_by'].choices = [('', 'Select who made the payment')]
                # Log the error for debugging
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error calculating remaining rent: {e}")
        else:
            # If no rent_record, set default choices
            self.fields['payment_by'].choices = [('', 'Select who made the payment')]
    
    def clean_amount_received(self):
        amount = self.cleaned_data.get('amount_received')
        if amount and self.rent_record:
            try:
                remaining = self.rent_record.remaining_rent
                if amount > remaining:
                    raise forms.ValidationError(f"Amount cannot exceed remaining rent of ₹{remaining}")
            except Exception as e:
                # If we can't calculate remaining rent, just validate the amount is positive
                if amount <= 0:
                    raise forms.ValidationError("Amount must be greater than 0")
        return amount