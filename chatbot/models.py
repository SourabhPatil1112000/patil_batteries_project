from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    BATTERY_TYPES = [
        ('INV', 'Inverter Battery'),
        ('SOL', 'Solar Battery'),
        ('CAR', 'Car Battery'),
        ('TUB', 'Tubular Battery'),
        ('LI', 'Lithium-ion Battery'),
    ]
    
    name = models.CharField(max_length=100)
    battery_type = models.CharField(max_length=3, choices=BATTERY_TYPES)
    capacity = models.CharField(max_length=50)
    voltage = models.CharField(max_length=20)
    warranty = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_battery_type_display()})"

class ChatPrompt(models.Model):
    prompt_text = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Chat Prompt (Updated: {self.last_updated})"