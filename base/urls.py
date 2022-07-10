from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IndexView, name='home'),
    path('login', views.Login, name="login"),
    path('signup', views.SignUp, name="sign-up"),
    path('logout/', views.Logout, name="logout"),
    
    path('ajax/getProductData', views.GetProductData, name="getProduct"),
    path('ajax/navData', views.GetNavData, name='getNavData'),

    path('browse/', views.AllProductPage, name="browse"),
    path('browse/<slug:slug>/', views.BrowseProductByBrandName, name="browse-products-brand"),
    path('product/<slug:slug>/', views.ProductPage, name="product-page"),
    path('search/', views.SearchProducts, name="search-products"),

    path('cart/', views.CartView, name='cart'),
    path('add-to-cart', views.AddToCart, name='add-to-cart'),
    path('delete-from-cart', views.DeleteFromCart, name='delete-from-cart'),

    path('checkout/', views.CheckoutView, name='checkout'),
    path('process/', views.ProcessOrder, name='process_order'),
    path('cart/success', views.Success, name='order-success'),
    path('stripe_webhook/', views.StripeWebhook, name='stripe-webhook')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)