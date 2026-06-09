from django.core.mail import send_mail
from twilio.rest import Client
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Avg, Q
from .models import Product, Category, Review, Order, OrderItem, ContactMessage
from decimal import Decimal
from django.http import JsonResponse
from django.conf import settings
import json
from groq import Groq

def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:6]
    categories = Category.objects.all()
    recent_reviews = Review.objects.filter(is_approved=True)[:6]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'bakery/home.html', context)


def get_cart_count(request):
    cart = request.session.get('cart', {})
    count = sum(cart.values())
    return JsonResponse({'count': count})

def products(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'bakery/products.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.filter(is_approved=True)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    related_products = Product.objects.filter(
        category=product.category, 
        is_available=True
    ).exclude(id=product.id)[:4]
    
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if customer_name and rating and comment:
            Review.objects.create(
                product=product,
                customer_name=customer_name,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Thank you for your review!')
            return redirect('product_detail', slug=slug)
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'related_products': related_products,
    }
    return render(request, 'bakery/product_detail.html', context)

def cart(request):
    cart_items = request.session.get('cart', {})
    products = []
    subtotal = Decimal('0.00')
    cart_product_ids = list(cart_items.keys())
    
    for product_id, quantity in cart_items.items():
        try:
            product = Product.objects.get(id=product_id)
            item_total = product.price * quantity
            products.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            subtotal += item_total
        except Product.DoesNotExist:
            pass
    
    # Calculate GST (18% for India) and total
    tax = subtotal * Decimal('0.18')
    total = subtotal + tax
    
    # Get recommended products (not already in cart)
    recommended_products = Product.objects.filter(
        is_available=True
    ).exclude(
        id__in=cart_product_ids
    ).order_by('?')[:3]
    
    context = {
        'cart_items': products,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
        'recommended_products': recommended_products,
    }
    return render(request, 'bakery/cart.html', context)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(product_id)
        
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        
        request.session['cart'] = cart
        messages.success(request, 'Product added to cart!')
        
        # Get the referer to redirect back
        referer = request.META.get('HTTP_REFERER', '')
        if 'products' in referer:
            return redirect('products')
        elif 'product' in referer:
            return redirect(referer)
        
        return redirect('cart')
    
    return redirect('products')

def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart[product_id] = quantity
        else:
            cart.pop(product_id, None)
        
        request.session['cart'] = cart
        messages.success(request, 'Cart updated!')
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    cart.pop(product_id, None)
    request.session['cart'] = cart
    messages.success(request, 'Product removed from cart!')
    return redirect('cart')

def checkout(request):
    cart_items = request.session.get('cart', {})
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    products = []
    subtotal = Decimal('0.00')
    
    for product_id, quantity in cart_items.items():
        try:
            product = Product.objects.get(id=product_id)
            item_total = product.price * quantity
            products.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            subtotal += item_total
        except Product.DoesNotExist:
            pass
    
    # Calculate tax and total
    tax = subtotal * Decimal('0.08')
    total = subtotal + tax
    
    if request.method == 'POST':
        order = Order.objects.create(
            customer_name=request.POST.get('customer_name'),
            customer_email=request.POST.get('customer_email'),
            customer_phone=request.POST.get('customer_phone'),
            delivery_address=request.POST.get('delivery_address', ''),
            is_delivery=request.POST.get('delivery_method') == 'delivery',
            special_instructions=request.POST.get('special_instructions', ''),
            payment_method=request.POST.get('payment_method', 'cash'),
            total_amount=total,
            status='confirmed'
        )
        
        for item in products:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
        
        request.session['cart'] = {}

        try:
            # ✅ Email to Customer
            send_mail(
                subject=f'🎉 Order #{order.id} Confirmed - Artisan Bakery',
                message=f'''
Hi {order.customer_name}!

Your order #{order.id} has been placed successfully! 🎉

Order Details:
━━━━━━━━━━━━━━━━━━━━
Total Amount: ₹{order.total_amount:.2f}
Payment Method: {order.payment_method.upper()}
Delivery: {"Home Delivery" if order.is_delivery else "Store Pickup"}
━━━━━━━━━━━━━━━━━━━━

Track your order anytime:
http://127.0.0.1:8000/track-order/

Order ID: {order.id}
Email: {order.customer_email}

Thank you for choosing Artisan Bakery! 🍰
                ''',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.customer_email],
                fail_silently=True,
            )

            # ✅ Email to Baker
            send_mail(
                subject=f'🔔 New Order #{order.id} Received!',
                message=f'''
New Order Alert! 🔔

Customer: {order.customer_name}
Phone: {order.customer_phone}
Email: {order.customer_email}
Total: ₹{order.total_amount:.2f}
Payment: {order.payment_method.upper()}
Delivery: {"Home Delivery" if order.is_delivery else "Store Pickup"}
{"Address: " + order.delivery_address if order.is_delivery else ""}
Special Instructions: {order.special_instructions or "None"}

Update order status:
http://127.0.0.1:8000/admin/bakery/order/{order.id}/change/
                ''',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.BAKERY_OWNER_EMAIL],
                fail_silently=True,
            )

            # ✅ WhatsApp to Baker
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                to=settings.BAKER_WHATSAPP_NUMBER,
                body=f'''🔔 *New Order Received!*

*Order ID:* #{order.id}
*Customer:* {order.customer_name}
*Phone:* {order.customer_phone}
*Total:* ₹{order.total_amount:.2f}
*Payment:* {order.payment_method.upper()}
*Delivery:* {"Home Delivery 🚚" if order.is_delivery else "Store Pickup 🏪"}
{"*Address:* " + order.delivery_address if order.is_delivery else ""}
*Special Instructions:* {order.special_instructions or "None"}

Update status: http://127.0.0.1:8000/admin/
                '''
            )

            # ✅ WhatsApp to Customer
            phone = order.customer_phone.strip().replace(' ', '').replace('-', '')
            if not phone.startswith('+'):
                phone = f'+91{phone}'
            client.messages.create(
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                to=f'whatsapp:{phone}',
                body=f'''🎉 *Order Confirmed - Artisan Bakery*

Hi {order.customer_name}!

Your order has been placed successfully! 🍰

*Order ID:* #{order.id}
*Total:* ₹{order.total_amount:.2f}
*Payment:* {order.payment_method.upper()}
*Delivery:* {"Home Delivery 🚚" if order.is_delivery else "Store Pickup 🏪"}

Track your order:
http://127.0.0.1:8000/track-order/

Thank you for choosing Artisan Bakery! 😊
                '''
            )

        except Exception as e:
            print(f"Notification error: {e}")

        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_confirmation', order_id=order.id)
    
    context = {
        'cart_items': products,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }
    return render(request, 'bakery/checkout.html', context)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'bakery/order_confirmation.html', context)

def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        messages.success(request, 'Thank you for contacting us! We\'ll get back to you soon.')
        return redirect('contact')
    
    return render(request, 'bakery/contact.html')

def about(request):
    return render(request, 'bakery/about.html')

def track_order(request):
    order = None
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        email = request.POST.get('email')
        try:
            order = Order.objects.get(id=order_id, customer_email=email)
        except Order.DoesNotExist:
            messages.error(request, 'Order not found! Please check your Order ID and Email.')
    
    context = {'order': order}
    return render(request, 'bakery/track_order.html', context)

def ai_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        # Get all products for context
        products = Product.objects.filter(is_available=True)
        product_list = "\n".join([
            f"- {p.name}: ₹{p.price} - {p.description[:80]}"
            for p in products
        ])
        
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a friendly assistant for a bakery shop.
Help customers find products, answer questions and suggest items.
Keep responses short, warm and helpful.
Our menu:
{product_list}"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=300
        )
        
        reply = response.choices[0].message.content
        return JsonResponse({'reply': reply})
    
    return JsonResponse({'error': 'POST required'}, status=400)