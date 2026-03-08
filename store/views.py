from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Laptop, Cart, CartItem, Order, OrderItem

import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth


# ==========================
# LAPTOP LIST
# ==========================
def laptop_list(request):
    laptops = Laptop.objects.all()
    return render(request, 'store/laptop_list.html', {'laptops': laptops})


# ==========================
# LAPTOP DETAIL
# ==========================
def laptop_detail(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    return render(request, 'store/laptop_detail.html', {'laptop': laptop})


# ==========================
# ADD TO CART
# ==========================
@login_required
def add_to_cart(request, laptop_id):

    laptop = get_object_or_404(Laptop, id=laptop_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        laptop=laptop
    )

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    return redirect('cart_view')


# ==========================
# VIEW CART
# ==========================
@login_required
def cart_view(request):

    cart, created = Cart.objects.get_or_create(user=request.user)

    items = cart.items.select_related('laptop')

    total = cart.total_price()

    return render(request, 'store/cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })


# ==========================
# INCREASE QUANTITY
# ==========================
def increase_quantity(request, item_id):

    item = CartItem.objects.get(id=item_id)
    item.quantity += 1
    item.save()

    return redirect('cart_view')


# ==========================
# DECREASE QUANTITY
# ==========================
def decrease_quantity(request, item_id):

    item = CartItem.objects.get(id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart_view')


# ==========================
# REMOVE ITEM
# ==========================
def remove_from_cart(request, item_id):

    item = CartItem.objects.get(id=item_id)
    item.delete()

    return redirect('cart_view')


# ==========================
# CHECKOUT PAGE
# ==========================
@login_required
def checkout_view(request):

    cart, created = Cart.objects.get_or_create(user=request.user)

    items = cart.items.select_related('laptop')

    if not items:
        return redirect('cart_view')

    total = cart.total_price()

    context = {
        'cart': cart,
        'items': items,
        'total': total
    }

    return render(request, 'store/checkout.html', context)


# ==========================
# MPESA ACCESS TOKEN
# ==========================
def get_access_token():

    consumer_key = "uAZJRpogfTvGqbsqVQoTnpl3Q2mSC3LX3MIdz2B554Hhm8mq"
    consumer_secret = "DDGdCjfWrVkgCu4kA1v9GSSBl3KLOwMTqx7DkVkU6MnEDOx3iJK0R3miwdA1GH1P"

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    return response.json()['access_token']


# ==========================
# MPESA STK PUSH
# ==========================
def stk_push(phone, amount):

    access_token = get_access_token()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    shortcode = "174379"
    passkey = "ACl1B0QVwy8CXrpmew4DDK5B2R8iBBtUGbDu4uHq5+VPR+I5gKokAUui1mM1sUhYQTGRDPO+FHX3xVg+lI+wvXHbOu4zoTlJVh6vdFoc+ZiuSC3GeOu1kVifYJ8INSslDUyWxghy5f9vzx2a18yD6TBQ5A0Cn2BxVo/OJ8GZIlYHsCiOSXUEu1qN2ydUK/r9LtnZn4m91hRTd9jYWgOnkbJrftG6F4xTbq5TpP+OHLP3Hrizgxcpy6BKrLkb1SWsluOow/PsO4bN6gYke8rPlaeS+YNyLbVFfyFbFz0VAfLL9pRpLWg5I45n1qswCXGsig5Ca76x0A3lROryXBxqAA=="

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    password = base64.b64encode(
        (shortcode + passkey + timestamp).encode()
    ).decode()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Convert phone number to 254 format
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+254"):
        phone = phone[1:]

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": "https://webhook.site",
        "AccountReference": "Laptop Store",
        "TransactionDesc": "Laptop Purchase"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Debug response
    print("MPESA RESPONSE:", response.text)

    try:
        return response.json()
    except:
        return {"error": response.text}


# ==========================
# PLACE ORDER
# ==========================
@login_required
def place_order(request):

    if request.method == "POST":

        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
        total = cart.total_price()

        phone = request.POST.get("phone")

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            phone=phone,
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            payment_method=request.POST.get("payment_method"),
            total_price=total
        )

        # Save order items
        for item in items:

            OrderItem.objects.create(
                order=order,
                laptop=item.laptop,
                quantity=item.quantity,
                price=item.laptop.price
            )

        # Send STK push
        response = stk_push(phone, 1)
        print("STK RESPONSE:", response)

        # Clear cart
        items.delete()

        return redirect('order_success')
def order_success(request):
    return render(request, "store/success.html")