from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import BaseUserManager, AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length = 100, null=True, blank=True)
    device = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        if self.username != None:
            return self.email  
        else:
            return str(self.device)

class Brand(models.Model):
    brand_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.brand_name

    def save(self, *args, **kwargs):
        value = self.brand_name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

class Category(models.Model):
    brand_name = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL)
    category_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        value = self.category_name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    brand_name = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL)
    category_name = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    colour = models.CharField(max_length=200)
    images = models.ImageField(default='default.jpg', upload_to='images')
    year_released = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        value = self.product_name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

class ProductAvailability(models.Model):
    product_name = models.ForeignKey(Product, null=True, on_delete= models.CASCADE)
    size = models.IntegerField()

    def __str__(self):
        return "%s | Size Available: %s" % (self.product_name, self.size)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    def final_price(self):
        if self.product.discount_price:
            return self.product.discount_price
        else:
            return self.product.price

class UserShippingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    postcode = models.CharField(max_length=8)
    alternate_email = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=11, blank=True, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def is_default(self):
        return self.default

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(UserShippingDetails, on_delete=models.SET_NULL, blank=True, null=True)
    order_amount = models.FloatField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    payment_intent = models.CharField(max_length=200)

    def __str__(self):
            return str(self.user)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return str(self.order)
