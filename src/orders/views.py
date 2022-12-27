from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 
                  'orders/order/detail.html',
                  {'order': order})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                order=order, 
                product=item['product'],
                price=item['price'],
                quantify = item['quantify']
                )
            # clear the cart
            cart.clear()
            #launch asynchronous task
            order_created.delay(order.id)
            #set the order in the session
            request.session['order_id'] = order.id
            #redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 
           'orders/order/create.html',
           {'cart': cart, 'form': form})