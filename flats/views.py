from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Flat, FlatMember, RentRecord, PaymentRecord
from .forms import FlatForm, FlatMemberForm, RentRecordForm, PaymentRecordForm

def owner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'owner':
            raise Http404("Page not found")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@owner_required
def add_flat(request):
    if request.method == 'POST':
        form = FlatForm(request.POST)
        if form.is_valid():
            flat = form.save(commit=False)
            flat.owner = request.user  # Set the current owner
            flat.save()
            messages.success(request, 'Flat added successfully!')
            return redirect('flats:manage_flats')
    else:
        form = FlatForm()
    
    return render(request, 'flats/add_flat.html', {'form': form})

@login_required
@owner_required
def add_flat_member(request, flat_id):
    flat = get_object_or_404(Flat, id=flat_id, owner=request.user)
    
    if request.method == 'POST':
        form = FlatMemberForm(request.POST, request.FILES, flat=flat)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Flat member added successfully!')
                return redirect('flats:flat_detail', flat_id=flat.id)
            except Exception as e:
                messages.error(request, f'Error creating flat member: {str(e)}')
    else:
        form = FlatMemberForm(flat=flat)
    
    return render(request, 'flats/add_flat_member.html', {'form': form, 'flat': flat})

@login_required
def flat_detail(request, flat_id):
    flat = get_object_or_404(Flat, id=flat_id)
    
    # Check permissions
    if request.user.user_type == 'renter':
        # Renter can only see their own flat
        if not flat.flat_members.filter(user=request.user).exists():
            raise Http404("Page not found")
    elif request.user.user_type == 'owner' and flat.owner != request.user:
        raise Http404("Page not found")  # Owner can only see their own flats
    
    # Get all related data
    members = flat.flat_members.all()
    rent_records = flat.rent_records.all().order_by('-month')
    
    # Get all payments for this flat
    all_payments = []
    for record in rent_records:
        payments = record.payment_records.all().order_by('-payment_date')
        all_payments.extend(payments)
    
    # Sort payments by date (most recent first)
    all_payments.sort(key=lambda x: x.payment_date, reverse=True)
    
    # Calculate flat statistics
    total_rent_records = rent_records.count()
    total_rent_amount = sum(record.total_rent for record in rent_records)
    total_received = sum(record.total_received for record in rent_records)
    total_pending = total_rent_amount - total_received
    
    # Get recent payments (last 10)
    recent_payments = all_payments[:10]
    
    # Get current month rent record
    from datetime import datetime
    current_month = datetime.now().replace(day=1)
    current_rent_record = rent_records.filter(month=current_month).first()
    
    return render(request, 'flats/flat_detail.html', {
        'flat': flat,
        'members': members,
        'rent_records': rent_records,
        'all_payments': all_payments,
        'recent_payments': recent_payments,
        'total_rent_records': total_rent_records,
        'total_rent_amount': total_rent_amount,
        'total_received': total_received,
        'total_pending': total_pending,
        'current_rent_record': current_rent_record
    })

# flats_list view removed

@login_required
@owner_required
def view_member_detail(request, member_id):
    """View detailed information about a specific flat member"""
    # Get the member and verify ownership
    member = get_object_or_404(FlatMember, id=member_id)
    
    # Ensure the current user is the owner of the flat
    if member.flat.owner != request.user:
        messages.error(request, "You don't have permission to view this member's details.")
        return redirect('accounts:dashboard')
    
    return render(request, 'flats/view_member_detail.html', {
        'member': member,
        'flat': member.flat
    })

@login_required
@owner_required
def update_member_detail(request, member_id):
    """Update information for a specific flat member"""
    # Get the member and verify ownership
    member = get_object_or_404(FlatMember, id=member_id)
    
    # Ensure the current user is the owner of the flat
    if member.flat.owner != request.user:
        messages.error(request, "You don't have permission to update this member's details.")
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = FlatMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f"{member.full_name}'s details have been updated successfully.")
            return redirect('flats:view_member_detail', member_id=member.id)
    else:
        form = FlatMemberForm(instance=member)
    
    return render(request, 'flats/update_member_detail.html', {
        'form': form,
        'member': member,
        'flat': member.flat
    })

@login_required
@owner_required
def manage_flats(request):
    """Manage flats - Management interface with edit/delete options"""
    flats = Flat.objects.filter(owner=request.user).prefetch_related('flat_members')
    
    # Calculate basic stats for each flat
    flat_stats = []
    for flat in flats:
        members_count = flat.flat_members.count()
        rent_records_count = flat.rent_records.count()
        
        flat_stats.append({
            'flat': flat,
            'members_count': members_count,
            'rent_records_count': rent_records_count
        })
    
    # High-level counts for header cards
    occupied_count = sum(1 for f in flats if f.flat_members.count() > 0)
    vacant_count = sum(1 for f in flats if f.flat_members.count() == 0)
    total_revenue = sum([f.monthly_rent for f in flats]) if flats else 0

    return render(request, 'flats/manage_flats.html', {
        'flats': flats,
        'flat_stats': flat_stats,
        'occupied_count': occupied_count,
        'vacant_count': vacant_count,
        'total_revenue': total_revenue,
        'view_type': 'management'
    })

@login_required
@owner_required
def manage_rent(request, flat_id):
    # Ensure the flat belongs to the current owner
    flat = get_object_or_404(Flat, id=flat_id, owner=request.user)
    
    if request.method == 'POST':
        form = RentRecordForm(request.POST, flat_id=flat_id)
        if form.is_valid():
            rent_record = form.save(commit=False)
            rent_record.flat = flat
            rent_record.save()
            messages.success(request, 'Rent record saved successfully!')
            return redirect('flats:flat_payment_records', flat_id=flat.id)
    else:
        form = RentRecordForm(initial={'monthly_rent': flat.monthly_rent}, flat_id=flat_id)
    
    rent_records = flat.rent_records.all()
    
    return render(request, 'flats/manage_rent.html', {
        'form': form,
        'flat': flat,
        'rent_records': rent_records
    })

@login_required
@owner_required
def edit_rent(request, record_id):
    # Ensure the rent record belongs to the current owner's flat
    record = get_object_or_404(RentRecord, id=record_id, flat__owner=request.user)
    
    if request.method == 'POST':
        form = RentRecordForm(request.POST, instance=record, flat_id=record.flat.id)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rent record updated successfully!')
            return redirect('flats:manage_rent', flat_id=record.flat.id)
    else:
        form = RentRecordForm(instance=record, flat_id=record.flat.id)
    
    return render(request, 'flats/edit_rent.html', {
        'form': form,
        'record': record,
        'flat': record.flat
    })

@login_required
@owner_required
def delete_rent(request, record_id):
    """Delete a rent record"""
    # Ensure the rent record belongs to the current owner's flat
    record = get_object_or_404(RentRecord, id=record_id, flat__owner=request.user)
    flat_id = record.flat.id
    
    if request.method == 'POST':
        # Check if there are any payments for this rent record
        payments_count = record.payment_records.count()
        if payments_count > 0:
            messages.warning(request, f'Cannot delete rent record. It has {payments_count} payment(s) associated with it. Please delete the payments first.')
            return redirect('flats:manage_rent', flat_id=flat_id)
        
        # Delete the rent record
        record.delete()
        messages.success(request, 'Rent record deleted successfully!')
        return redirect('flats:manage_rent', flat_id=flat_id)
    
    return render(request, 'flats/delete_rent.html', {
        'record': record,
        'flat': record.flat
    })

@login_required
@owner_required
def add_payment(request, record_id):
    """Add payment for a rent record"""
    rent_record = get_object_or_404(RentRecord, id=record_id, flat__owner=request.user)
    
    if request.method == 'POST':
        form = PaymentRecordForm(request.POST, rent_record=rent_record)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.rent_record = rent_record
            payment.save()
            messages.success(request, 'Payment recorded successfully!')
            return redirect('flats:flat_payment_records', flat_id=rent_record.flat.id)
    else:
        form = PaymentRecordForm(rent_record=rent_record)
    
    return render(request, 'flats/add_payment.html', {
        'form': form,
        'rent_record': rent_record,
        'flat': rent_record.flat
    })

@login_required
@owner_required
def edit_payment(request, payment_id):
    """Edit a payment record"""
    payment = get_object_or_404(PaymentRecord, id=payment_id, rent_record__flat__owner=request.user)
    
    if request.method == 'POST':
        form = PaymentRecordForm(request.POST, instance=payment, rent_record=payment.rent_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment updated successfully!')
            return redirect('flats:flat_payment_records', flat_id=payment.rent_record.flat.id)
    else:
        form = PaymentRecordForm(instance=payment, rent_record=payment.rent_record)
    
    return render(request, 'flats/edit_payment.html', {
        'form': form,
        'payment': payment,
        'rent_record': payment.rent_record,
        'flat': payment.rent_record.flat
    })

@login_required
@owner_required
def delete_payment(request, payment_id):
    """Delete a payment record"""
    payment = get_object_or_404(PaymentRecord, id=payment_id, rent_record__flat__owner=request.user)
    flat_id = payment.rent_record.flat.id
    
    if request.method == 'POST':
        payment.delete()
        messages.success(request, 'Payment deleted successfully!')
        return redirect('flats:flat_payment_records', flat_id=flat_id)
    
    return render(request, 'flats/delete_payment.html', {
        'payment': payment,
        'rent_record': payment.rent_record,
        'flat': payment.rent_record.flat
    })

@login_required
@owner_required
def payment_summary(request):
    """Dashboard showing comprehensive payment summary for all flats in card layout"""
    # Get all flats for the current owner
    flats = Flat.objects.filter(owner=request.user)
    
    # Get all rent records for all flats
    all_rent_records = RentRecord.objects.filter(flat__owner=request.user)
    
    # Calculate comprehensive statistics
    total_flats = flats.count()
    total_rent_records = all_rent_records.count()
    
    # Calculate total amounts across all months
    total_rent_amount = sum(record.total_rent for record in all_rent_records)
    total_received_amount = sum(record.total_received for record in all_rent_records)
    total_pending_amount = sum(record.remaining_rent for record in all_rent_records)
    
    # Count payment status across all records
    paid_records = sum(1 for record in all_rent_records if record.remaining_rent <= 0)
    partial_records = sum(1 for record in all_rent_records if record.total_received > 0 and record.remaining_rent > 0)
    unpaid_records = sum(1 for record in all_rent_records if record.total_received == 0)
    
    payment_stats = {
        'total_flats': total_flats,
        'total_rent_records': total_rent_records,
        'total_rent_amount': total_rent_amount,
        'total_received_amount': total_received_amount,
        'total_pending_amount': total_pending_amount,
        'paid_records': paid_records,
        'partial_records': partial_records,
        'unpaid_records': unpaid_records,
    }
    
    # Get detailed flat information
    flat_payment_status = []
    for flat in flats:
        flat_rent_records = flat.rent_records.all()
        flat_total_rent = sum(record.total_rent for record in flat_rent_records)
        flat_total_received = sum(record.total_received for record in flat_rent_records)
        flat_total_pending = sum(record.remaining_rent for record in flat_rent_records)
        
        # Get the last payment date across all records for this flat
        last_payment = PaymentRecord.objects.filter(rent_record__flat=flat).order_by('-payment_date').first()
        last_payment_date = last_payment.payment_date if last_payment else None
        
        # Determine overall status for this flat
        if flat_total_pending <= 0:
            status = 'paid'
        elif flat_total_received > 0:
            status = 'partial'
        else:
            status = 'not_paid'
        
        flat_payment_status.append({
            'flat': flat,
            'rent_records_count': flat_rent_records.count(),
            'total_rent': flat_total_rent,
            'received': flat_total_received,
            'remaining': flat_total_pending,
            'last_payment_date': last_payment_date,
            'status': status,
        })
    
    return render(request, 'flats/payment_summary.html', {
        'payment_stats': payment_stats,
        'flat_payment_status': flat_payment_status,
    })

@login_required
@owner_required
def flat_payment_records(request, flat_id):
    """Display all payment records for a specific flat"""
    # Get the flat and verify ownership
    flat = get_object_or_404(Flat, id=flat_id, owner=request.user)
    
    # Get all rent records for this flat
    rent_records = RentRecord.objects.filter(flat=flat).order_by('-month')
    
    # Calculate flat statistics
    total_rent = sum(record.total_rent for record in rent_records)
    total_received = sum(record.total_received for record in rent_records)
    total_pending = sum(record.remaining_rent for record in rent_records)
    
    # Get all payments for this flat
    payments = PaymentRecord.objects.filter(rent_record__flat=flat).order_by('-payment_date')
    
    # Count payment status
    paid_records = sum(1 for record in rent_records if record.remaining_rent <= 0)
    partial_records = sum(1 for record in rent_records if record.total_received > 0 and record.remaining_rent > 0)
    unpaid_records = sum(1 for record in rent_records if record.total_received == 0)
    
    flat_stats = {
        'total_rent': total_rent,
        'total_received': total_received,
        'total_pending': total_pending,
        'paid_records': paid_records,
        'partial_records': partial_records,
        'unpaid_records': unpaid_records,
        'total_records': rent_records.count(),
    }
    
    return render(request, 'flats/flat_payment_records.html', {
        'flat': flat,
        'rent_records': rent_records,
        'payments': payments,
        'payment_stats': flat_stats,
    })

@login_required
@owner_required
def delete_flat(request, flat_id):
    """Delete a flat and all associated data"""
    # Ensure the flat belongs to the current owner
    flat = get_object_or_404(Flat, id=flat_id, owner=request.user)

    if request.method == 'POST':
        flat_number = flat.flat_number
        # Delete the flat (cascade will handle related data)
        flat.delete()
        messages.success(request, f'Flat {flat_number} and all associated data deleted successfully!')
        return redirect('flats:manage_flats')

    # Get statistics for confirmation
    members_count = flat.flat_members.count()
    rent_records_count = flat.rent_records.count()
    total_payments = sum(record.payment_records.count() for record in flat.rent_records.all())

    return render(request, 'flats/delete_flat.html', {
        'flat': flat,
        'members_count': members_count,
        'rent_records_count': rent_records_count,
        'total_payments': total_payments
    })

@login_required
@owner_required
def comprehensive_payment_summary(request):
    """Comprehensive payment summary showing all payments across all months"""
    # Get all flats for the current owner
    flats = Flat.objects.filter(owner=request.user)
    
    # Get all rent records for all flats
    all_rent_records = RentRecord.objects.filter(flat__owner=request.user)
    
    # Calculate comprehensive statistics
    total_flats = flats.count()
    total_rent_records = all_rent_records.count()
    
    # Calculate total amounts
    total_rent_amount = sum(record.total_rent for record in all_rent_records)
    total_received_amount = sum(record.total_received for record in all_rent_records)
    total_pending_amount = sum(record.remaining_rent for record in all_rent_records)
    
    # Count payment status
    paid_records = sum(1 for record in all_rent_records if record.remaining_rent <= 0)
    partial_records = sum(1 for record in all_rent_records if record.total_received > 0 and record.remaining_rent > 0)
    unpaid_records = sum(1 for record in all_rent_records if record.total_received == 0)
    
    comprehensive_stats = {
        'total_flats': total_flats,
        'total_rent_records': total_rent_records,
        'total_rent_amount': total_rent_amount,
        'total_received_amount': total_received_amount,
        'total_pending_amount': total_pending_amount,
        'paid_records': paid_records,
        'partial_records': partial_records,
        'unpaid_records': unpaid_records,
    }
    
    # Get detailed flat information
    flat_details = []
    for flat in flats:
        flat_rent_records = flat.rent_records.all()
        flat_total_rent = sum(record.total_rent for record in flat_rent_records)
        flat_total_received = sum(record.total_received for record in flat_rent_records)
        flat_total_pending = sum(record.remaining_rent for record in flat_rent_records)
        
        flat_details.append({
            'flat': flat,
            'rent_records_count': flat_rent_records.count(),
            'total_rent': flat_total_rent,
            'total_received': flat_total_received,
            'total_pending': flat_total_pending,
            'rent_records': flat_rent_records,
        })
    
    return render(request, 'flats/comprehensive_payment_summary.html', {
        'comprehensive_stats': comprehensive_stats,
        'flat_details': flat_details,
    })

@login_required
def payment_history(request, record_id):
    """View payment history for a specific rent record"""
    rent_record = get_object_or_404(RentRecord, id=record_id)
    
    # Check permissions
    if request.user.user_type == 'renter':
        # Renter can only see their own flat's records
        if not rent_record.flat.flat_members.filter(user=request.user).exists():
            raise Http404("Page not found")
    elif request.user.user_type == 'owner' and rent_record.flat.owner != request.user:
        raise Http404("Page not found")  # Owner can only see their own flats
    
    payments = rent_record.payment_records.all()
    
    # Check for potential duplicate payments (same amount on same day)
    duplicate_warnings = []
    payment_groups = {}
    
    for payment in payments:
        key = f"{payment.amount_received}_{payment.payment_date.date()}"
        if key not in payment_groups:
            payment_groups[key] = []
        payment_groups[key].append(payment)
    
    for key, group in payment_groups.items():
        if len(group) > 1:
            duplicate_warnings.append({
                'amount': group[0].amount_received,
                'date': group[0].payment_date.date(),
                'payments': group,
                'count': len(group)
            })
    
    return render(request, 'flats/payment_history.html', {
        'rent_record': rent_record,
        'payments': payments,
        'flat': rent_record.flat,
        'duplicate_warnings': duplicate_warnings
    })

@login_required
@owner_required
def bulk_delete_payments(request, record_id):
    """Bulk delete duplicate payments for a rent record"""
    rent_record = get_object_or_404(RentRecord, id=record_id, flat__owner=request.user)
    
    if request.method == 'POST':
        payment_ids = request.POST.getlist('payment_ids')
        if payment_ids:
            payments_to_delete = PaymentRecord.objects.filter(
                id__in=payment_ids,
                rent_record=rent_record
            )
            deleted_count = payments_to_delete.count()
            payments_to_delete.delete()
            messages.success(request, f'Successfully deleted {deleted_count} payment(s).')
            return redirect('flats:payment_history', record_id=record_id)
    
    # Get duplicate payments
    payments = rent_record.payment_records.all()
    payment_groups = {}
    
    for payment in payments:
        key = f"{payment.amount_received}_{payment.payment_date.date()}"
        if key not in payment_groups:
            payment_groups[key] = []
        payment_groups[key].append(payment)
    
    duplicate_groups = []
    for key, group in payment_groups.items():
        if len(group) > 1:
            duplicate_groups.append({
                'amount': group[0].amount_received,
                'date': group[0].payment_date.date(),
                'payments': group,
                'count': len(group)
            })
    
    return render(request, 'flats/bulk_delete_payments.html', {
        'rent_record': rent_record,
        'duplicate_groups': duplicate_groups,
        'flat': rent_record.flat
    })