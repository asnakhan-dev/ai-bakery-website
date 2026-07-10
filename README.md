# Artisan Bakery
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-purple?style=for-the-badge)](https://ai-bakery-website-1.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-green?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Groq](https://img.shields.io/badge/Groq-Llama%204%20Scout%2017B-orange?style=for-the-badge)](https://groq.com)

> A production-ready AI-powered bakery e-commerce platform built with Django, Groq, Twilio WhatsApp API, UPI Payments, and Render.


https://github.com/user-attachments/assets/4e777cfe-fe4b-4c0b-9ee0-fc13669473f0


## Live Demo

**Application**

https://ai-bakery-website-1.onrender.com

> Hosted on Render's free tier. The initial request may take 30–60 seconds if the service is starting after inactivity.

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

![Admin Dashboard](https://github.com/user-attachments/assets/e92f1e76-9e3e-49f8-a030-9eb4a00d2e57)

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
c

### Order Processing Workflow

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
```
---

## Key Features

### AI Integration
- **Groq API + LLaMA 4 Scout 17B** — Conversational AI bakery assistant
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

## System Architecture

```text             Customer
                        │
                        ▼
        HTML • CSS • JavaScript (Frontend)
                        │
                        ▼
               Django Backend
                        │
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                 ▼
 AI Chatbot       Order Management   Admin Dashboard
      │                 │                 │
      ▼                 ▼                 ▼
 Groq API        SQLite Database   Order Processing
      │                 │
      └────────────┬────┘
                   ▼
      Email & WhatsApp Notifications
                   │
                   ▼
                Customer
```

---


## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0 (Python 3.11) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| AI / LLM | Groq API — LLaMA 4 Scout 17B |
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

- **Model:** LLaMA 4 Scout 17B (via Groq API)
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

## Engineering Challenges

- Integrating LLM APIs (Groq) into a Django backend
- Twilio WhatsApp Business API for real-time notifications
- Production deployment with environment-based config
- Debugging Gunicorn worker timeouts in production
- Django Admin customization with signal-based notifications
- Mobile-responsive CSS without a framework

---

<div align="center">

Built with Django · Groq · Twilio · Render

<br>

**Portfolio Project**

This repository is intended for portfolio and educational demonstration purposes only. The source code may not be copied, redistributed, or submitted as your own work without the author's permission.

<br>

© 2026 Asna Khan. All rights reserved.

</div>

