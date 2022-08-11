import stripe
import json
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import User, Brand, Product, ProductAvailability, Cart, UserShippingDetails, OrderItem, Order
from django.db.models import Q
from .forms import UserForm

def SignUp(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = UserForm
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            # if the user had created a cart before signing in - we need to transfer this cart to there username 
            try:
                device = request.COOKIES['device']
                user_device = User.objects.get(device = device)
                # if so, then we can change and assign the cart back to the user order
                cart = Cart.objects.filter(user = user_device).update(user=user)
                # and then can delete the device user object
                user_device.delete()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # if the user had nothing in their cart - we can login straight away
            except:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            return redirect('/')

    context = {'form': form}
    return render(request, 'signup.html', context)


def Login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_object = User.objects.get(email=email)
        except:
            messages.error(request, 'Email does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            try:
                # checking if they have anything in there cart prior to logging in 
                device = request.COOKIES['device']
                user_device = User.objects.get(device = device)
                # if so, then we can change and assign the cart back to the user order
                cart = Cart.objects.filter(user = user_device).update(user=user_object)
                # and then we can delete the device user object (as it was created for temporary use)
                user_device.delete()
            except:
                print("Nothing was inserted into to the cart, prior to logging in")

            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username and Password does not exist')

    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('login')

# AJAX - GETS recents addition from the products table 
def GetProductData(request):
    if request.method == "GET":
        # get the latest object inserted into database and live updates the html (should not use in deployment)
        product = Product.objects.all().order_by('-created')[:10]
        return JsonResponse({"product":list(product.values())})

# Using AJAX to load the nav bar data dynamically
def GetNavData(request):
    if request.method == "GET":
        latest_product = Product.objects.all().order_by('-created')[:10]
        discount_product = Product.objects.exclude(discount_price__isnull=True)[:10]
        try:
            try:
                products_in_cart = Cart.objects.filter(user = request.user).count()
            except:
                device = request.COOKIES['device']
                user = User.objects.get(device = device)
                products_in_cart = Cart.objects.filter(user = user).count()
        except:
            products_in_cart = '' 
    return JsonResponse({"latest_product":list(latest_product.values()), "discount_product":list(discount_product.values()), "products_in_cart": products_in_cart})


def IndexView(request):
    latest_product = Product.objects.all().order_by('-created')[:10]
    brand_names = Brand.objects.all()
    
    context = {'brand_names':brand_names, 'latest_product': latest_product}
    return render(request, 'home.html', context)

def AllProductPage(request):
    products = Product.objects.all()
    product_count = products.count()   
    
    brand = "All Shoes"
    all_brand_names = Brand.objects.all()

    context =  {'brand': brand,'all_brand_names':all_brand_names, 'products': products, 'product_count': product_count}

    return render(request, 'content.html', context)


def BrowseProductByBrandName(request, slug):
    # getting name affiliated with the slug above
    brand = Brand.objects.get(slug=slug) 
    # and then using that brand name to get all shoes which are affiliated to it
    products= Product.objects.filter(brand_name=brand)
    product_count = products.count()   
    
    context = {'brand': brand, 'products': products, 'product_count':product_count}

    return render(request, 'content.html', context)

def SearchProducts(request):
    if request.method == "POST":
        search = request.POST['search']
        
        products = Product.objects.filter(
            Q(product_name__icontains=search) | 
            Q(brand_name__brand_name__icontains=search) |
            Q(category_name__category_name__icontains=search) |
            Q(colour__icontains=search) 
        )

        product_count = products.count()  
        context = {'search': search, 'products': products, 'product_count': product_count}
        return render(request, 'content.html', context)
    else:
        context = {}
        return render(request, 'content.html', context)

def ProductPage(request, slug):
    product = Product.objects.get(slug=slug)
    product_availability = ProductAvailability.objects.filter(product_name=product).order_by('size')
   
    context = {'product': product, 'product_availability': product_availability}
    return render(request, 'product.html', context)


def CartView(request):
    products_in_cart = ""

    try:
        try:
            cart = Cart.objects.filter(user = request.user)
            products_in_cart = len(cart)
        except:
            device = request.COOKIES['device']
            user = User.objects.get(device = device)
            cart = Cart.objects.filter(user = user)
            products_in_cart = len(cart)

        if products_in_cart == 0:
            cart = "Empty"
    except:
        cart = "Empty"


    context = {'cart': cart, 'products_in_cart': products_in_cart}
    return render(request, 'cart.html', context)

def AddToCart(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product_size = request.POST.get('product_size')

        # check if the product exist
        check_product_exist = Product.objects.get(id=product_id)
        if(check_product_exist):
            # check if the product size is available
            check_product_size = ProductAvailability.objects.get(product_name=product_id, size=product_size)
            if(check_product_size):
                try:
                    Cart.objects.create(user=request.user, product_id=product_id, size=product_size)
                    products_in_cart = Cart.objects.filter(user = request.user).count()
                    return JsonResponse({'status': 'Item has been succesfully added to Cart', 'products_in_cart': products_in_cart })
                except:
                    # if the user is not logged in - we can use cookies to track this users cart
                    device = request.COOKIES['device']
                    user, created = User.objects.get_or_create(device=device)
                    cart = Cart.objects.create(user=user, product_id=product_id, size=product_size)
                   
                    products_in_cart = Cart.objects.filter(user=user).count()
                    return JsonResponse({'status': 'Item has been succesfully added to Cart', 'products_in_cart': products_in_cart })
            else:
                return JsonResponse({'status': 'Product size is not available'})
        else:
            return JsonResponse({'status': 'Product does not exist'})   
    return redirect('home')

def DeleteFromCart(request):
    if request.method == "POST":
        cart_id = int(request.POST.get('cart_id'))
        try:
            try:
                cart = Cart.objects.filter(id=cart_id, user=request.user)
                cart.delete()   
                return JsonResponse({'status': 'success'})
            except:
                device = request.COOKIES['device']
                user = User.objects.get(device = device)
                cart = Cart.objects.filter(id=cart_id, user = user)
                cart.delete() 
                return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'No Item exist to remove'})

    return redirect('home')

@login_required(login_url='login')
def CheckoutView(request):
    try:
        shipping_details = UserShippingDetails.objects.get(user=request.user, default=True)
    except:
        shipping_details = None

    try:
        try:
            # first checking if the user added to his/her cart when they were not signed on
            device = request.COOKIES['device']
            user = User.objects.get(device = device)
            # if so, then we can change and assign the cart back to the user order
            cart = Cart.objects.filter(user = user) 
            cart.user = request.user
            cart.save()
            # and then we can delete the device user object (as this is a temporary object)
            user.delete()
        except:
            cart = Cart.objects.filter(user = request.user)
    except:
        return redirect('')
    
    public_key = settings.STRIPE_API_KEY_PUBLIC

    context = {'cart': cart, 'public_key': public_key, 'shipping_details': shipping_details}
    return render(request, 'checkout.html', context)

@login_required(login_url='login')
def ProcessOrder(request):
    # first get all items in cart
    cart = Cart.objects.filter(user = request.user)
    total_amount= 0
    items = []
    data = json.loads(request.body)
    # create the cart into a json object for stripe
    for item in cart:
        product_name = item.product
        # coverting pound to pennies - so i can process it in stripe
        product_price = item.final_price() * 100
        product_price = int(product_price)
        
        total_amount += item.final_price()

        obj = {
            'price_data':{
                'currency': 'gbp',
                'product_data':{
                    'name': product_name
                },
                'unit_amount': product_price
            },
            'quantity': 1
        }   

        items.append(obj)

    # start the stripe process
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = items,
        mode = 'payment',
        success_url = 'http://127.0.0.1:8000/cart/success',
        cancel_url = 'http://127.0.0.1:8000/cart/success',
    )
    payment_intent = session.payment_intent

    # get the data which the user passes into customer detail form (if they use there default address, data varaible will return with default address is true)
    if data['default_address'] == 'True':
        shipping_details = UserShippingDetails.objects.get(user = request.user, default = True)
    else:
    # user details
        first_name = data['firstname']
        last_name = data['lastname']
        address = data['address']
        postcode = data['postcode']
        city = data['city']
        alternate_email = data['email']
        number = data['number']
        default = data['default']

        if default == True:
            # check if a default address exist first (as i have made it that you can only have one current default address)
            try:
                change_default_shipping = UserShippingDetails.objects.get(user = request.user, default = True)
            except:
                change_default_shipping = ''

            # if we do find a default address in the database, we will change it to default equals false
            if len(change_default_shipping) > 0:
                change_default_shipping.default = False
                change_default_shipping.save()

            shipping_details = UserShippingDetails.objects.create(
                user = request.user, first_name = first_name, last_name = last_name, street_address = address, city = city, postcode =  postcode, alternate_email = alternate_email, number = number, default = True
            )

        # if the user inserts a new address, but doesnt want to change their default address - we make the default value equal false
        else:
            shipping_details = UserShippingDetails.objects.create(
                user = request.user, first_name = first_name, last_name = last_name, street_address = address, city = city, postcode =  postcode, alternate_email = alternate_email, number = number, default = False
            )

    # creating the actual order
    order = Order.objects.create(
        user = request.user,
        order_amount = total_amount
    )
    order.shipping_address = shipping_details
    order.payment_intent = payment_intent
    order.save()
 
    # create the items in order
    for item in cart:
        product = item.product
        product_size = item.size
        price = item.final_price()
        item = OrderItem.objects.create(
            order = order,
            product = product,
            size = product_size,
            price = price
        )
    
    return JsonResponse({'session': session, 'order': payment_intent})

# use a webhook to verify payment (is a must for this website to function properly)
# stripe listen --forward-to localhost:8000/stripe_webhook/
@csrf_exempt
def StripeWebhook(request):
    endpoint_secret = ""

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session.payment_status == "paid":
            payment_intent = session['payment_intent']
            # if checkout has been completed - we can change the order to paid/ and can delete the cart made by the user 
            order = Order.objects.get(payment_intent = payment_intent)
            order.paid = True
            order.save()

            # delete the cart as payment was successful
            cart = Cart.objects.filter(user = order.user)
            cart.delete()

    #elif event["type"] == "payment_intent.succeeded":
        #session = event['data']['object']
       
    return HttpResponse(status=200)


@login_required(login_url='login')
def Success(request):
    order = ''
    order_status = ''

    try:
        order = Order.objects.filter(user = request.user).order_by('-created')[0]
        items_in_order = OrderItem.objects.filter(order = order)
    except:
        order = None
        items_in_order = None

    # check if the order was paid for - if so then delete the cart created by the user 
    # can also be done in the webhook - just need to send the username/ user id as meta data 
    if order != None:
        if order.paid != True:
            order.delete()
            check_if_default = order.shipping_address.is_default()
            print(check_if_default)
            if check_if_default == False:
                order.shipping_address.delete()
        else:
            order_status = 'Pass'    
        
    context = {'order': order, 'items_in_order': items_in_order, 'order_status': order_status}
    return render(request, 'success.html', context)
