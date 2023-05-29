from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart 
from .tasks import order_created


def order_create(request):
    """requesting the current cart"""
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart: # for an item in the cart, create...
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            order_created(order.id)
            return render(request,
                         'orders/order/created.html',
                         {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                 'orders/order/create.html',
                 {'cart': cart, 'form': form})
