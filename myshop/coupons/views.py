from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Coupon
from .forms import CouponApplyForms


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForms(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, # captions not taken into account
                                        valid_from__lte=now, # lower or equal
                                        valid_to__gte=now, # grater or equal
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')

# Create your views here.
