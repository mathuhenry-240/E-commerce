from itertools import product
from multiprocessing import context
from sqlite3 import complete_statement
from urllib import request
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

# Create your views here.


def storeview(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_carttotal': 0, 'shipping': False}
        cartitems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartitems': cartitems}
    return render(request, 'store/store.html', context)


def cartview(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_carttotal': 0, 'shipping': False}
        cartitems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'store/cart.html', context)


def checkoutview(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_carttotal': 0, 'shipping': False}
        cartitems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartitems': cartitems}

    return render(request, 'store/checkout.html', context)


def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer)
    orderitem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_carttotal:
            order.complete == True
        order.save()

        if order.shipping == True:
            ShippingAdress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode']
            )
    return JsonResponse('payment complete', safe=False)
