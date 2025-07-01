from django.shortcuts import render,redirect,get_object_or_404
from .models import Order,OrderedItem,Address
from products.models import Product
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages


# Create your views here.
def show_cart(request):
    user=request.user
    customer=user.customer_profile
    cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE

    )
    saved_address = Address.objects.filter(owner=customer, order=cart_obj).last()
    address_exists = saved_address is not None
    context={
        'cart':cart_obj,
        'address_exists': address_exists,
        'saved_address': saved_address,
        }

    return render(request,'cart.html',context)
@login_required(login_url='account')
def remove_from_cart(request,pk):

    item = get_object_or_404(OrderedItem, pk=pk)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')

@login_required(login_url='account')
def checkout_cart(request):
    if request.POST:
        try:
            user=request.user
            customer=user.customer_profile
            total = float(request.POST.get('total'))
            order_obj=Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE

            )
            if order_obj:
                order_obj.order_status = Order.ORDER_CONFIRMED
                order_obj.total_price = total
                order_obj.save()

                return render(request,'success.html')
        except Exception as e:
                return render(request,'success.html')








@login_required(login_url='account')
def add_to_cart(request):
    if request.POST:
        user=request.user
        customer=user.customer_profile
        quantity=int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')
        cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE

        )
        product = Product.objects.get(pk=product_id)
        ordered_item,created=OrderedItem.objects.get_or_create(
        product=product,
        size=size,
        owner=cart_obj,
        )
        if created:
            ordered_item.quantity=quantity
            ordered_item.save()
        else:
            ordered_item.quantity=ordered_item.quantity+quantity
            ordered_item.save()

    return redirect('cart')

@login_required(login_url='account')
def start_payment(request):

    customer = request.user.customer_profile
    order = Order.objects.filter(owner=customer, order_status=Order.CART_STAGE).order_by('-created_at').first()
    total_amount = int(sum(item.product.price * item.quantity for item in order.added_items.all()) * 100)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    
    payment = client.order.create({
        "amount": total_amount,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        'cart': order,
        'payment': payment,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'total_amount': total_amount,
    }
    return render(request, 'payment.html', context)




@login_required(login_url='account')
def view_orders(request):
    user = request.user
    customer=user.customer_profile
    all_orders = Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders': all_orders}
    return render(request, 'orders.html',context)

@login_required(login_url='account')
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, owner=request.user.customer_profile)
    return render(request, 'track_order.html', {'order': order})

@login_required(login_url='account')
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, owner=request.user.customer)
    
    # Optional: Generate and return PDF invoice (placeholder here)
    # Use libraries like WeasyPrint, xhtml2pdf, or ReportLab
    from django.http import HttpResponse
    return HttpResponse(f"Invoice for Order #{order.id} - (To be implemented)", content_type="text/plain")



@login_required(login_url='account')
@csrf_protect
def save_address(request):
    if request.method == 'POST':
        user = request.user
        customer = user.customer_profile
        order = Order.objects.filter(owner=customer, order_status=Order.CART_STAGE).first()

        is_edit = request.POST.get('is_edit') == 'True'

        if is_edit:
            # Update existing address
            address = Address.objects.filter(owner=customer, order=order).last()
            if address:
                address.full_name = request.POST.get('full_name')
                address.phone = request.POST.get('phone')
                address.address_line = request.POST.get('address_line')
                address.city = request.POST.get('city')
                address.state = request.POST.get('state')
                address.postal_code = request.POST.get('postal_code')
                address.country = request.POST.get('country')
                address.save()
                messages.success(request, "Address updated successfully.")
        else:
            # Create new address
            Address.objects.create(
                full_name=request.POST.get('full_name'),
                phone=request.POST.get('phone'),
                address_line=request.POST.get('address_line'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                postal_code=request.POST.get('postal_code'),
                country=request.POST.get('country'),
                owner=customer,
                order=order
            )
            messages.success(request, "Address saved successfully.")

        return redirect('cart')
