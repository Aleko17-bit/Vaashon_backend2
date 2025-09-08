from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# -------------------
# Profile Model
# -------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

# -------------------
# Category Model
# -------------------
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    def __str__(self):
        return self.name

# -------------------
# Product Model
# -------------------
class Product(models.Model):
    SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)
    available_sizes = models.CharField(
        max_length=20,
        blank=True,
        help_text="Comma-separated sizes, e.g., S,M,L,XL"
    )

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        if self.sale_price and self.price:
            return round((self.price - self.sale_price) / self.price * 100)
        return 0

    @property
    def display_price(self):
        return self.sale_price if self.sale_price else self.price

    def get_size_list(self):
        """Return a list of available sizes."""
        if self.available_sizes:
            return self.available_sizes.split(',')
        return []

# -------------------
# Review Model
# -------------------
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

# -------------------
# CartItem Model
# -------------------
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    size = models.CharField(max_length=5, blank=True, null=True)  # selected size
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} × {self.product.name} ({self.size})"

    @property
    def total_price(self):
        return self.quantity * self.product.display_price

# -------------------
# Order Model
# -------------------
class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Paid', 'Paid'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    size = models.CharField(max_length=5, blank=True, null=True)  # selected size
    quantity = models.PositiveIntegerField(default=1)
    address = models.TextField(blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='COD')
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} ({self.size})"

    @property
    def total_price(self):
        return self.quantity * (self.product.display_price if self.product else 0)

# -------------------
# Payment Model
# -------------------
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_payments", null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=50,
        choices=(
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("failed", "Failed"),
        ),
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"
