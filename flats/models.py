from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

class Flat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_flats', limit_choices_to={'user_type': 'owner'}, null=True, blank=True)
    flat_number = models.CharField(max_length=10)
    floor = models.IntegerField(validators=[MinValueValidator(0)])
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=0, default=6000 )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Flat {self.flat_number} (Owner: {self.owner.username if self.owner else 'No Owner'})"
    
    @property
    def total_people(self):
        """Total number of people living in this flat"""
        return self.flat_members.count()
    
    @property
    def main_renter(self):
        """Get the main renter (the one with login access)"""
        return self.flat_members.filter(is_main_renter=True).first()
    
    class Meta:
        ordering = ['flat_number']
        unique_together = ['owner', 'flat_number']  # Flat number unique per owner

class FlatMember(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='flat_members')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, help_text="Main user account for this flat (only one per flat)")
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    aadhar_number = models.CharField(max_length=12, unique=True)
    pan_number = models.CharField(max_length=10, unique=True)
    aadhar_document = models.FileField(upload_to='documents/aadhar/', blank=True)
    pan_document = models.FileField(upload_to='documents/pan/', blank=True)
    other_documents = models.FileField(upload_to='documents/other/', blank=True)
    is_main_renter = models.BooleanField(default=False, help_text="Main renter who has login access")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the member")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.flat}"
    
    class Meta:
        ordering = ['-is_main_renter', 'full_name']

class RentRecord(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='rent_records')
    month = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(0)])
    electricity_units = models.DecimalField(max_digits=8, decimal_places=0, default=0, validators=[MinValueValidator(0)])
    electricity_rate = models.DecimalField(max_digits=6, decimal_places=0, default=8, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['flat', 'month']
        ordering = ['-month']
    
    @property
    def electricity_bill(self):
        return self.electricity_units * self.electricity_rate
    
    @property
    def total_rent(self):
        return self.monthly_rent + self.electricity_bill
    
    @property
    def total_received(self):
        """Total amount received for this rent record"""
        try:
            return sum(payment.amount_received for payment in self.payment_records.all())
        except Exception:
            return 0
    
    @property
    def remaining_rent(self):
        """Remaining amount to be paid"""
        try:
            return self.total_rent - self.total_received
        except Exception:
            return self.total_rent
    
    @property
    def is_fully_paid(self):
        """Check if rent is fully paid"""
        return self.remaining_rent <= 0
    
    @property
    def payment_status(self):
        """Get payment status"""
        if self.is_fully_paid:
            return 'paid'
        elif self.total_received > 0:
            return 'partial'
        else:
            return 'unpaid'
        
    def __str__(self):
        return f"{self.flat} - {self.month.strftime('%B %Y')}"

class PaymentRecord(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
        ('cheque', 'Cheque'),
        ('online', 'Online Payment'),
    ]
    
    rent_record = models.ForeignKey(RentRecord, on_delete=models.CASCADE, related_name='payment_records')
    amount_received = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(0)])
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='cash')
    payment_by = models.CharField(max_length=100, help_text="Name of the person who made the payment")
    notes = models.TextField(blank=True, help_text="Additional notes about the payment")
    
    class Meta:
        ordering = ['-payment_date']
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.amount_received and self.amount_received <= 0:
            raise ValidationError("Amount received must be greater than 0.")
    
    def save(self, *args, **kwargs):
        # Only validate remaining rent if we have a rent_record set
        if self.rent_record and self.amount_received:
            try:
                remaining = self.rent_record.remaining_rent
                if self.amount_received > remaining:
                    from django.core.exceptions import ValidationError
                    raise ValidationError(f"Amount received cannot exceed remaining rent amount of ₹{remaining}.")
            except Exception:
                pass  # Let form validation handle this
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Payment of ₹{self.amount_received} for {self.rent_record} on {self.payment_date.strftime('%d/%m/%Y')}"

