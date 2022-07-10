from django.contrib import admin
from .models import User, Brand, Category, Product, ProductAvailability, Cart, UserShippingDetails, Order, OrderItem

admin.site.register(User)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductAvailability)
admin.site.register(Cart)
admin.site.register(UserShippingDetails)
admin.site.register(Order)
admin.site.register(OrderItem)
