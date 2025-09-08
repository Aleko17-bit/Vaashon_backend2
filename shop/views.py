from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product, Category, CartItem, Order, Payment, Profile
from .serializer import ProductSerializer, CategorySerializer, CartItemSerializer, OrderSerializer

import requests
import base64
from datetime import datetime
import json

# ----------------------
# Terms & Privacy Pages
# ----------------------
def terms_view(request):
    return render(request, 'shop/terms.html')

def privacy_view(request):
    return render(request, 'shop/privacy.html')

# ----------------------
# Twilio SMS
# ----------------------
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

# ----------------------
# Helper Functions
# ----------------------
def send_order_email(user_email, username, total, payment_method, orders=None):
    if not user_email:
        return
    product_lines = ""
    if orders:
        for order in orders:
            price = order.product.sale_price if order.product.sale_price else order.product.price
            product_lines += f"• {order.product.name} x {order.quantity} (Size: {order.size}) - KES {price * order.quantity:.2f}\n"
    message = (
        f"🎉 Hello {username}! 🎉\n\n"
        f"Thank you for shopping with Vaashon Shop! We’re thrilled to confirm your order.\n\n"
        f"🛒 Your Products:\n{product_lines}\n"
        f"💰 Total: KES {total:.2f}\n"
        f"💳 Payment method: {payment_method}\n\n"
        f"✨ We can’t wait for you to enjoy your purchase! ✨\n\n"
        f"💖 With love,\nVaashon Shop Team"
    )
    try:
        send_mail(
            subject='Your Vaashon Shop Order Confirmation 🎉',
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER),
            recipient_list=[user_email],
            fail_silently=False,
        )
    except Exception as e:
        print("Email sending failed:", e)

def send_order_sms(phone_number, username, total):
    if not TWILIO_AVAILABLE or not phone_number:
        return
    try:
        client = Client(
            getattr(settings, 'TWILIO_ACCOUNT_SID', ''),
            getattr(settings, 'TWILIO_AUTH_TOKEN', '')
        )
        client.messages.create(
            body=f'Vaashon Shop: Hi {username}, your order totaling KES {total:.2f} has been placed successfully!',
            from_=getattr(settings, 'TWILIO_PHONE_NUMBER', ''),
            to=phone_number
        )
    except Exception as e:
        print("SMS sending failed:", e)

# ----------------------
# HTML Views
# ----------------------
def home(request):
    category_id = request.GET.get('category')
    query = request.GET.get('q', '')

    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_id:
        products = products.filter(category_id=category_id)
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'shop/home.html', {
        'categories': categories,
        'products': products,
        'selected_category': category_id,
        'search_query': query
    })

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email or not password:
            return render(request, 'shop/register.html', {"error": "Email and password are required."})
        if User.objects.filter(email=email).exists():
            return render(request, 'shop/register.html', {"error": "Email already registered."})
        username = email.split("@")[0]
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'shop/register.html')

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'shop/login.html', {"error": "Invalid email or password."})
    return render(request, 'shop/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def product_detail(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return redirect('home')
    in_stock = product.available and product.quantity > 0
    return render(request, 'shop/product_detail.html', {'product': product, 'in_stock': in_stock})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.filter(id=product_id, available=True).first()
    if not product:
        return redirect('home')
    selected_size = request.POST.get("size")
    if not selected_size:
        return redirect('product_detail', product_id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        size=selected_size
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def update_cart_quantity(request, item_id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart_item = CartItem.objects.filter(id=item_id, user=request.user).first()
        if cart_item:
            cart_item.quantity = max(quantity, 1)
            cart_item.save()
    return redirect('cart')

@login_required
def update_cart_size(request, item_id):
    if request.method == "POST":
        size = request.POST.get("size")
        cart_item = CartItem.objects.filter(id=item_id, user=request.user).first()
        if cart_item and size:
            cart_item.size = size
            cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        item.price = item.product.sale_price if item.product.sale_price else item.product.price
        item.total = item.price * item.quantity
    grand_total = sum(item.total for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'grand_total': grand_total})

@login_required
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('home')

    total = sum((item.product.sale_price if item.product.sale_price else item.product.price) * item.quantity for item in cart_items)
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method", "COD")
        phone_number = request.POST.get("phone", "").strip()
        user_email = request.user.email or request.POST.get("email", "").strip()
        profile.phone_number = phone_number
        profile.save()

        if not phone_number:
            return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total, 'error': 'Phone number is required.'})
        if not user_email:
            return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total, 'error': 'Email address is required.'})

        orders = []
        for item in cart_items:
            order = Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                size=item.size,
                address='',
                payment_method=payment_method,
                paid=False,
                status='Processing' if payment_method == 'COD' else 'Pending'
            )
            orders.append(order)

        cart_items.delete()
        send_order_email(user_email, request.user.username, total, payment_method, orders)
        send_order_sms(phone_number, request.user.username, total)

        if payment_method == "COD":
            return render(request, "shop/order_success.html", {"message": f"Order placed successfully! A confirmation email has been sent to {user_email}."})
        if payment_method == "ONLINE":
            request.session["order_ids"] = [o.id for o in orders]
            return JsonResponse({"order_ids": [o.id for o in orders]})

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders})

def category_products(request, category_id):
    category = Category.objects.filter(id=category_id).first()
    if not category:
        return redirect('home')
    products = Product.objects.filter(category=category, available=True)
    categories = Category.objects.all()
    return render(request, 'shop/home.html', {
        'categories': categories,
        'products': products,
        'selected_category': category
    })

# ----------------------
# API Views
# ----------------------
@api_view(["GET"])
def product_list(request):
    products = Product.objects.filter(available=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart_items_api(request):
    cart = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(cart, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart_api(request):
    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_list_api(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# ----------------------
# MPESA STK PUSH & CALLBACK
# ----------------------
@login_required
def stk_push(request):
    order_ids = request.session.get("order_ids", [])
    if not order_ids:
        return JsonResponse({"error": "No orders to process."})

    profile = getattr(request.user, 'profile', None)
    phone_number = getattr(profile, "phone_number", None)
    if not phone_number:
        return JsonResponse({"error": "User phone number not set."})

    total_amount = sum((o.product.sale_price if o.product.sale_price else o.product.price) * o.quantity for o in Order.objects.filter(id__in=order_ids))

    try:
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        r = requests.get(auth_url, auth=(consumer_key, consumer_secret))
        access_token = json.loads(r.text).get('access_token')

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        short_code = settings.MPESA_SHORTCODE
        passkey = settings.MPESA_PASSKEY
        password = base64.b64encode((short_code + passkey + timestamp).encode()).decode('utf-8')

        stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        callback_url = settings.MPESA_CALLBACK_URL

        payload = {
            "BusinessShortCode": short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": total_amount,
            "PartyA": phone_number,
            "PartyB": short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": f"OrderBatch-{','.join(map(str, order_ids))}",
            "TransactionDesc": "Payment for goods"
        }

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(stk_url, json=payload, headers=headers)
        res_json = response.json()

        checkout_id = res_json.get("CheckoutRequestID")
        if checkout_id:
            for order in Order.objects.filter(id__in=order_ids):
                order.transaction_id = checkout_id
                order.save()

        return JsonResponse(res_json)

    except Exception as e:
        print("STK Push error:", e)
        return JsonResponse({"error": str(e)})

@csrf_exempt
def daraja_callback(request):
    try:
        data = json.loads(request.body)
        stk = data.get('Body', {}).get('stkCallback', {})
        callback_metadata = stk.get('CallbackMetadata', {}).get('Item', [])

        amount = 0
        mpesa_code = ""
        if callback_metadata:
            for item in callback_metadata:
                if item.get('Name') == 'Amount':
                    amount = item.get('Value', 0)
                if item.get('Name') == 'MpesaReceiptNumber':
                    mpesa_code = item.get('Value', '')

        checkout_id = stk.get('CheckoutRequestID', 'N/A')
        result_code = stk.get('ResultCode', 1)

        payment = Payment.objects.create(
            transaction_id=checkout_id,
            amount=amount,
            status="completed" if result_code == 0 else "failed"
        )

        orders = Order.objects.filter(transaction_id=checkout_id)
        for order in orders:
            order.paid = result_code == 0
            order.status = "Processing" if result_code == 0 else "Failed"
            order.save()
            payment.order = order
            payment.user = order.user
            payment.save()

    except Exception as e:
        print("Daraja callback error:", e)
        return HttpResponse(status=400)

    return HttpResponse("Success", status=200)

