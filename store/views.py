from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
import json
import datetime

from .models import *
from .form import *

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

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('store')
    else:
        form = UserCreationForm
    return render(request, "store/signup.html", {"form":form})

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



def login(request):
    #logic for navbar
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order['get_cart_items']
    
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('store/store.html') 
        else:
            messages.error(request, 'Invalid login credentials.')

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "store/login.html", context)

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

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order = order, created = Order.objects.get_or_create(customer=customer, completed=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

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

