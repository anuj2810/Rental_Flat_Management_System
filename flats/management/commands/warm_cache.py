from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.cache import cache
from flats.utils import get_payment_stats, get_optimized_rent_records

User = get_user_model()

class Command(BaseCommand):
    help = 'Warm up cache with frequently accessed data'

    def handle(self, *args, **options):
        self.stdout.write('Starting cache warming...')
        
        # Get all owners
        owners = User.objects.filter(user_type='owner')
        
        for owner in owners:
            # Warm up payment stats cache
            cache_key = f'payment_stats_{owner.id}'
            rent_records = get_optimized_rent_records(owner)
            stats = get_payment_stats(rent_records, cache_key)
            
            self.stdout.write(f'Warmed cache for owner: {owner.username}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully warmed cache for all owners')
        )