def calculate_payment_stats(rent_records):
    """Centralized payment statistics calculation"""
    return rent_records.aggregate(
        total_rent=Sum('total_rent'),
        total_received=Sum('total_received'),
        total_pending=Sum('remaining_rent')
    )