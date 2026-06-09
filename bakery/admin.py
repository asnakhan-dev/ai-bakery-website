from django.contrib import admin
from .models import Category, Product, Review, Order, OrderItem, ContactMessage
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_featured', 'is_available']
    list_filter = ['category', 'is_featured', 'is_available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'product', 'rating', 'created_at', 'is_approved']
    list_filter = ['rating', 'is_approved', 'created_at']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'status', 'payment_method', 'total_amount', 'created_at']
    list_filter = ['status', 'is_delivery', 'created_at', 'payment_method']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_editable = ['status']

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            status_messages = {
                'confirmed': '✅ Your order has been confirmed!',
                'preparing': '👨‍🍳 Our chefs are baking your order right now!',
                'ready': '🎉 Your order is ready for pickup/delivery!',
                'completed': '😊 Your order has been delivered! Enjoy!',
                'cancelled': '❌ Unfortunately your order has been cancelled.',
            }
            msg = status_messages.get(obj.status, '')
            if msg:
                try:
                    # ✅ Email to customer
                    send_mail(
                        subject=f'Order #{obj.id} Update - {obj.get_status_display()} 🍰',
                        message=f'''
Hi {obj.customer_name}!

{msg}

Order #{obj.id} Status: {obj.get_status_display()}

Track your order:
http://127.0.0.1:8000/track-order/

Use:
Order ID: {obj.id}
Email: {obj.customer_email}

Thank you for choosing Artisan Bakery! 🍰
                        ''',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[obj.customer_email],
                        fail_silently=True,
                    )

                    # ✅ WhatsApp to customer
                    client = Client(
                        settings.TWILIO_ACCOUNT_SID,
                        settings.TWILIO_AUTH_TOKEN
                    )
                    client.messages.create(
                        from_=settings.TWILIO_WHATSAPP_NUMBER,
                        to=f'whatsapp:+91{obj.customer_phone}',
                        body=f'''🍰 *Artisan Bakery - Order Update*

Hi {obj.customer_name}!

{msg}

*Order ID:* #{obj.id}
*Status:* {obj.get_status_display()}

Track your order:
http://127.0.0.1:8000/track-order/

Thank you for choosing us! 😊
                        '''
                    )
                except Exception as e:
                    print(f"Notification error: {e}")
        super().save_model(request, obj, form, change)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']