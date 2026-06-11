# Artisan Bakery — AI-Powered Bakery E-Commerce Platform



https://github.com/user-attachments/assets/4e777cfe-fe4b-4c0b-9ee0-fc13669473f0



> A production-ready, full-stack bakery e-commerce platform with an AI-powered chatbot, real-time order tracking, UPI payment integration, and automated WhatsApp + Email notifications — built and deployed by a fresher in under 2 weeks.

## Live Demo

**[ai-bakery-website-1.onrender.com](https://ai-bakery-website-1.onrender.com)**

> Note: Free tier on Render — first load may take 30-60 seconds to spin up.

---

## Demo Video

> Watch the full walkthrough: Home → Products → Cart → Checkout → Order Tracking → AI Chatbot

[Click to watch demo video](https://youtu.be/MG5MeYRHBXM?si=gPaSdbWdyYEZFpve)

---

## Notification System in Action

### WhatsApp Notifications (Twilio API)

#### Baker Alert
![Baker_WhatsApp](https://github.com/user-attachments/assets/5f4c32c7-4166-4090-ad07-73ccad0a57a2)

#### Customer Confirmation
![Customer_WhatsApp](https://github.com/user-attachments/assets/c631d320-b007-4fd6-b0e3-57d5da165c40)

### Email Notifications (Gmail SMTP)

#### New Order Alert to Baker
![Baker_Email](https://github.com/user-attachments/assets/723a4de7-8c10-4386-833e-88cb664fe7fd)

#### Order Confirmation to Customer
![Customer_Email](https://github.com/user-attachments/assets/bf6e8bab-7dcb-42ea-9c1f-981ff409ea5a)

---

## Admin Dashboard

The bakery owner manages the entire store through Django Admin.

### Features
- Add, edit, and remove products
- Manage categories
- View customer orders
- Update order status (Confirmed → Preparing → Ready → Delivered)
- Automatic Email notifications on status changes
- Automatic WhatsApp notifications on status changes
- View customer reviews
- View contact form submissions

  ---

### Order Management Features

- View and manage all customer orders
- Update order status in real time
- Filter orders by status, delivery type, payment method, and date
- View customer details and order summaries
- Manage products and categories
- View customer reviews
- Access contact form submissions
  
---

### Real-Time Status Workflow

```text
Order Placed
      │
      ▼
Confirmed
      │
      ▼
Preparing
      │
      ▼
Ready
      │
      ▼
Delivered

### Workflow

Customer places order
        │
        ▼
Django Admin Dashboard
        │
        ▼
Update Order Status
        │
        ├──► Email Notification
        └──► WhatsApp Notification

---

## Key Features

### AI Integration
- **Groq API + LLaMA 3.3 70B** — Conversational AI bakery assistant
- Context-aware — knows your entire product menu in real time
- Animated chef UI with quick-action buttons
- Handles product recommendations, ingredient queries, birthday suggestions

### E-Commerce
- Full product catalog with category filtering and search
- Session-based shopping cart with quantity controls
- Secure checkout with real-time form validation
- Indian phone number validation (+91 prefix enforced)

### Payment
- Cash on Delivery (COD)
- UPI Payment with dynamic QR code
- Deep links for PhonePe, Google Pay, Paytm, BHIM
- QR code auto-generates with exact order amount

### Order Management
- Real-time order status timeline (Confirmed → Preparing → Ready → Delivered)
- Auto-confirmed on placement
- Dynamic tracking — pickup vs delivery text updates automatically
- Baker updates status from Django Admin → customer notified instantly

### Notification System
- Customer receives Email + WhatsApp on order placement
- Baker receives Email + WhatsApp alert instantly
- Customer notified via Email + WhatsApp on every status change
- Each notification in isolated try/except — one failure never blocks others

### Deployment
- Deployed on Render with environment-based configuration
- WhiteNoise for static file serving
- Gunicorn WSGI server
- All secrets managed via environment variables (never hardcoded)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0 (Python 3.11) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| AI / LLM | Groq API — LLaMA 3.3 70B Versatile |
| Notifications | Twilio WhatsApp API + Django SMTP (Gmail) |
| Payment | UPI Deep Links + Dynamic QR Code |
| Database | SQLite (dev) |
| Static Files | WhiteNoise |
| Server | Gunicorn |
| Hosting | Render (Free Tier) |
| Version Control | Git + GitHub |

---

## Project Structure

```
bakery_project/
├── bakery/
│   ├── templates/bakery/        # 9 HTML templates
│   │   ├── base.html            # Global navbar, footer, AI chatbot widget
│   │   ├── home.html            # Landing page with image carousel
│   │   ├── products.html        # Product catalog with filters
│   │   ├── product_detail.html  # Product page with reviews
│   │   ├── cart.html            # Shopping cart
│   │   ├── checkout.html        # Checkout with UPI + COD
│   │   ├── order_confirmation.html  # Real-time order tracking
│   │   ├── track_order.html     # Order lookup by ID + Email
│   │   └── contact.html        # Contact form
│   ├── static/bakery/
│   │   ├── images/              # Product + UPI payment logos
│   │   └── css/                 # Custom styles
│   ├── models.py                # Product, Order, Review, Category models
│   ├── views.py                 # All business logic + AI + notifications
│   ├── urls.py                  # URL routing
│   └── admin.py                 # Custom admin with status-based notifications
├── bakery_project/
│   ├── settings.py              # Environment-based configuration
│   └── urls.py
├── requirements.txt
├── .gitignore
└── manage.py
```

---

## Local Setup

### Prerequisites
- Python 3.11+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/asnakhan-dev/ai-bakery-website.git
cd ai-bakery-website/bakery_project

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (see below)

# 5. Run migrations
python manage.py migrate

# 6. Create superuser (for admin access)
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

---

## Environment Variables

Create a `.env` file in `bakery_project/`:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

# AI Chatbot
GROQ_API_KEY=your-groq-api-key

# WhatsApp Notifications
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
BAKER_WHATSAPP_NUMBER=whatsapp:+91XXXXXXXXXX

# Email Notifications
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
BAKERY_OWNER_EMAIL=your-gmail@gmail.com
EMAIL_TIMEOUT=5
```

---

## How the Notification Flow Works

```
Customer places order
        │
        ├──► Customer receives Email (order confirmation + tracking link)
        ├──► Customer receives WhatsApp (order ID, total, delivery method)
        ├──► Baker receives Email (customer details, order summary)
        └──► Baker receives WhatsApp (instant alert with admin link)
                │
                ▼
        Baker updates status in Django Admin
                │
                ├──► Customer receives Email (status update)
                └──► Customer receives WhatsApp (status update)
```

---

## Pages & URLs

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Landing page with auto-playing image carousel |
| Products | `/products/` | Full catalog with category filter + search |
| Product Detail | `/product/<slug>/` | Product info + customer reviews |
| Cart | `/cart/` | Cart with quantity controls + recommendations |
| Checkout | `/checkout/` | COD + UPI payment with QR code |
| Order Confirmation | `/order-confirmation/<id>/` | Real-time tracking timeline |
| Track Order | `/track-order/` | Lookup by Order ID + Email |
| Contact | `/contact/` | Contact form (saved to DB) |
| Admin | `/admin/` | Baker dashboard — update order status |
| AI Chat | `/ai-chat/` | REST endpoint for chatbot |

---

## AI Chatbot Details

- **Model:** LLaMA 3.3 70B Versatile (via Groq API)
- **Context:** Entire product menu injected into system prompt at runtime
- **UI:** Floating animated chef widget with typing indicator
- **Quick Actions:** Cakes, Cookies, Birthday suggestions, Budget options
- **Response time:** ~1-2 seconds (Groq is extremely fast)

---

## Deployment Notes

Deployed on **Render Free Tier**:
- Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start command: `gunicorn bakery_project.wsgi`
- All secrets set as environment variables in Render dashboard
- WhiteNoise serves static files in production
- Email timeout set to 5 seconds to prevent Gunicorn worker timeout

---

## What I Learned Building This

- Integrating LLM APIs (Groq) into a Django backend
- Twilio WhatsApp Business API for real-time notifications
- Production deployment with environment-based config
- Debugging Gunicorn worker timeouts in production
- Django Admin customization with signal-based notifications
- Mobile-responsive CSS without a framework

---

## Developer

**Asna Khan**
B.Tech Graduate | Python Developer | AI Application Developer
Pune, India

- GitHub: [github.com/asnakhan-dev](https://github.com/asnakhan-dev)
- Live Project: [ai-bakery-website-1.onrender.com](https://ai-bakery-website-1.onrender.com)

---

## License

Copyright © 2026 Asna Khan.

All Rights Reserved.

This project is provided for portfolio and demonstration purposes only.
No part of this code may be copied, modified, distributed, or used without explicit written permission from the author.
