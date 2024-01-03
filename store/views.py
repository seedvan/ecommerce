from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
import json
import datetime
from .models import *
from .forms import *

#This function handles the logic for the store page
def store(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

#This function handles the logic for the shopping cart
def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

#This function handles the logic for the shopping cart
def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

#This function handles the logic for the registration/sign up page
def signup(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']
    
    #Registration logic
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            #form.save()
            login(request)
            return redirect('login')
    else:
        form = RegisterForm()

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'form':form}
    return render(request, "store/signup.html", context)

#This function handles the logic behind the product listing pages
def productdetails(request, pk):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']

    product = Product.objects.get(pk=pk)
    
    context={'items':items, 'order':order, 'product':product, 'cartItems':cartItems}
    return render(request, 'store/product.html', context)

#This function handles the logic behind a user's profile page
def profile(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        orders=customer.get_orders()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']
        orders=[]

    for order in orders:
        order.total = order.get_order_total()

    products = Product.objects.all()
        
    context = {'products':products, 'cartItems':cartItems, 'orders':orders, 'customer':customer, }
    return render(request, 'store/profile.html', context)

#This function handles the logic behind the login page. Note the authentication process is handled by built in Django authentication modules
def login(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "registration/login.html", context)

#This function defines the search page logic
def search(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    
    #This part of the function specifically handles the User's query into the search bar form
    form = SearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Product.objects.filter(
            Q(name__icontains=query) 
            )
    

    context = {'products':results, 'cartItems':cartItems, 'form': form, 'results': results}
    return render(request, 'store/search.html', context)

#This function handles the logic behind updating the Shopping cart
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

#This function handles the logic behind processing a customers order
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order = order, created = Order.objects.get_or_create(customer=customer, completed=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.completed=True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            county=data['shipping']['county'],
            postcode=data['shipping']['postcode'],
        )
    else:
        print('User is not logged in')
    return JsonResponse('Payment complete', safe=False)





    

