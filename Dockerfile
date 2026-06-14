# Python 3.11 ka clean lightweight environment
FROM python:3.11-slim

# Container ke andar ek folder banega jahan code jayega
WORKDIR /app

# Pehle sirf requirements copy karega
COPY requirements.txt .

# Sab libraries install karega
RUN pip install --no-cache-dir -r requirements.txt

# Ab baaki saara project copy karega
COPY . .

# Port 8000 open karega
EXPOSE 8000

# App start karega — same command jo Render pe tha
CMD ["gunicorn", "bakery_project.wsgi:application", "--bind", "0.0.0.0:8000"]