# Ecommerce Website
Ecommerce Store inspired by Laced and Footlocker 

Technology used:
- Django
- HTML, CSS
- Javascript
- AJAX (JS)
- DOM Manipulation
- Stripe API, Stripe Webhook

## Application
![home](https://user-images.githubusercontent.com/92265482/184150824-7b257498-9ab8-4d3d-9a7c-0dc247dee93a.gif)
If the end user has inserted their contact details before, and has ticked the default address box, it will save the details as being default. So when an new order is placed by the end user, they do not need retype their contact details (unless specified). 
![purchase](https://user-images.githubusercontent.com/92265482/184155329-401d3198-0497-4d23-9adc-3a09eafd8211.gif)
![image](https://user-images.githubusercontent.com/92265482/184163051-4c020bf0-b5ed-41a2-be4e-ca682ea166b8.png)
Here we can see the user has placed an order, and has chosen an alternative address. However payment failed, this was due to the fact our webhook was not setup in this image (by purpose), to show the outcome of inserting incorrect details in stripe.
![payment-failure](https://user-images.githubusercontent.com/92265482/184157234-bfe20db6-485a-4f47-a043-8c1e2fb24898.gif)
We can also add items in a shopping cart without the need of signing in through the use of cookies (whereby we are allocating an id to the end users technology) - however if the user wants to place an order, he/she has to sign in.
![cart](https://user-images.githubusercontent.com/92265482/184161497-1dbbbaa6-b95b-4a03-bcaa-4f24eb34d1de.gif)
If the product is not in stock (i.e there is not size available) - the following will be displayed
![image](https://user-images.githubusercontent.com/92265482/184162636-d66fe763-169d-4af9-b91c-f780a7bce656.png)

## Setup
### Installation
Python and Django need to be installed to run the the website
 
`pip install django`
 
### Usage
To run the program - open the directory that stores the application (and run the command below in the terminal)
 
`python manage.py runserver`
 
The website will be located in the browser: http://127.0.0.1:8000/
 
### Login
To create a superuser, run the command in the terminal and follow steps that appear
 
`python manage.py createsuperuser`
 
### Admin
To add products to the website and images, we have to login to the admin page with the superuser credentials created above.
 
The admin will be located in the browser at: http://127.0.0.1:8000/admin
 
### Payment
For payments to work, we need a Stripe API Key (found in your stripe dashboard, both a public and private key is needed) - we can either hard code them into the code under the setting.py file or as environment variable (have been commented out, under the setting.py file).
 
We also have to set up a Stripe Webhook, to make sure the payment page appears and card payments have been processed. To test this we can create a temporary webhook - follow the link for instructions:https://stripe.com/docs/webhooks/test.
 
The webhook secret has to be inserted in the views.py file and exactly under the function StripeWebhook. To run webhook, enter the following command in stripe CLI:
 
`stripe listen --forward-to localhost:8000/stripe_webhook/`
 
## Future
The website currently is not responsive and does not adjust depending on user screen size - therefore it is extremely important to add this functionality, as for the website to be set up in a real environment this is critical (and especially if it is a ecommerce store).
 
Another adjustment needed is to create an order after a payment has been made and not before. This will make it so if the user does cancel their order (by closing the payment page), there isn't an order created for that end user (thus keeping our database size at a minimum).
