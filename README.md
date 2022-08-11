# Ecommerce Website
Ecommerce Store inspired by Laced and Footlocker 
Technology used:
- Django
- HTML, CSS
- Javascript
- Ajax (JS)
- DOM Manipulation
- Stripe API, Stripe Webhook

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
 
## Application
![home](https://user-images.githubusercontent.com/92265482/184150824-7b257498-9ab8-4d3d-9a7c-0dc247dee93a.gif)

![purchase](https://user-images.githubusercontent.com/92265482/184155329-401d3198-0497-4d23-9adc-3a09eafd8211.gif)

## Future
The website currently is not responsive and does not adjust depending on user screen size - therefore it is extremely important to add this functionality, as for the website to be set up in a real environment this is critical (and especially if it is a ecommerce store).
 
Another adjustment needed is to create an order after a payment has been made and not before. This will make it so if the user does cancel their order (by closing the payment page), there isn't an order created for that end user (thus keeping our database size at a minimum).
