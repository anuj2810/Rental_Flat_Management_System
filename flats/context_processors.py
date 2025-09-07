from typing import Dict, Any
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from .models import FlatMember

User = get_user_model()

def footer_contact(request: HttpRequest) -> Dict[str, Any]:
    """Inject contact details for footer.
    - If user is a renter, show their owner's contact (owner of the renter's flat)
    - If user is an owner, show their own contact
    - Otherwise, return empty, so template can fallback
    """
    contact = {}

    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return {"footer_contact": contact}

    owner = None
    try:
        if getattr(user, 'user_type', '') == 'renter':
            # Find the flat this renter belongs to and get the owner
            member = FlatMember.objects.select_related('flat__owner').filter(user=user).first()
            if member and member.flat and member.flat.owner:
                owner = member.flat.owner
        elif getattr(user, 'user_type', '') == 'owner':
            owner = user
    except Exception:
        owner = None

    if owner:
        contact = {
            'name': (owner.first_name or '').strip() + ((' ' + owner.last_name) if owner.last_name else ''),
            'username': owner.username,
            'phone': getattr(owner, 'phone_number', '') or '',
            'email': owner.email or '',
        }

    return {"footer_contact": contact}