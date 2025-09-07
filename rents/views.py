from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from flats.models import Flat, FlatMember, RentRecord, PaymentRecord
from django.db.models import Sum

@login_required
def renter_rent_history(request):
    if request.user.user_type != 'renter':
        raise Http404("Page not found")

    try:
        # Find the flat where this user is a member
        flat_member = FlatMember.objects.get(user=request.user)
        flat = flat_member.flat
        rent_records = flat.rent_records.all().prefetch_related('payment_records')

        # Calculate totals
        total_rent_amount = sum(record.total_rent for record in rent_records)
        total_paid = sum(record.total_received for record in rent_records)
        total_pending = sum(record.remaining_rent for record in rent_records)

        # Get all payment records for this flat
        all_payments = []
        for record in rent_records:
            for payment in record.payment_records.all():
                all_payments.append({
                    'payment': payment,
                    'rent_record': record,
                    'month': record.month
                })

        # Sort payments by date (most recent first)
        all_payments.sort(key=lambda x: x['payment'].payment_date, reverse=True)

        # Calculate payment statistics (properties, not DB fields)
        paid_records = sum(1 for r in rent_records if r.is_fully_paid)
        partial_records = sum(1 for r in rent_records if (r.total_received > 0 and r.remaining_rent > 0))
        unpaid_records = sum(1 for r in rent_records if r.total_received == 0)

        return render(request, 'rents/renter_rent_history.html', {
            'flat': flat,
            'renter': flat_member,
            'rent_records': rent_records,
            'all_payments': all_payments,
            'total_rent_amount': total_rent_amount,
            'total_paid': total_paid,
            'total_pending': total_pending,
            'paid_records': paid_records,
            'partial_records': partial_records,
            'unpaid_records': unpaid_records,
        })
    except FlatMember.DoesNotExist:
        messages.error(request, 'Flat member profile not found.')
        return redirect('accounts:dashboard')