import datetime
from http.client import responses
import json
from tkinter.tix import Tree
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
import requests
from django.urls import reverse
from .models import OrderItem
import xmlrpc.client

url = 'http://127.0.0.1:8000/api'

def shop_page(request):
    response_category = requests.get(f'{url}/category/').json()
    response_products = requests.get(f'{url}/products/').json()
    attributes = requests.get(f'{url}/attribute/').json()

    return render(request, 'shop/shop-grid.html', {
        'category' : response_category, 
        'products' : response_products,
        'attributes' : attributes['Color'],})

def category(request, category):

    response_category_list = requests.get(f'{url}/category/').json()
    response_category = requests.get(f'{url}/category/{category}').json()
    response_products = requests.get(f'{url}/products/').json()
    attributes = requests.get(f'{url}/attribute/').json()

    categoryId = None

    if response_category != []:
        for elem in response_category:
            categoryId = elem['id']

    nb_elem = 0
    for product in response_products:
        if product['categ_id'][0] == categoryId:
            nb_elem = nb_elem +1

    return render (request, 'shop/category.html', {'category_list' : response_category_list,
                                                    'category' : response_category,
                                                    'products' : response_products, 
                                                    'categoryId' : categoryId,
                                                    'name' : category,
                                                    'attributes' : attributes['Color'],
                                                    'nb' : nb_elem,
                                                    })

def details (request, id):
    response_category_list = requests.get(f'{url}/category/').json() # Liste des category
    response_products = requests.get(f'{url}/products/').json()
    response = requests.get(f'{url}/products/{str(id)}').json() # Details du produit
    ids_alternatif = response[0]['product_template_image_ids'] # Ids des images alternatives
    allternatif_response = requests.get(f'{url}/alternatif/').json()

    imgs_alt=[]
    for alt in allternatif_response:
        if alt ['id'] in ids_alternatif:
            imgs_alt.append({'1920' : alt['image_1920'] , '128' : alt['image_128']})

    description = response[0]['description']

    # Product's Category
    categ_id = response[0]['categ_id'][0]
    for list in response_category_list :
        if list['id'] == categ_id :
            category = list['name']

    return render (request, 'shop/shop-details.html', {'product' : response,
                                                        'products' : response_products,
                                                        'category_list' : response_category_list,
                                                        'description' : description,
                                                        'alternatif' : imgs_alt,
                                                        'nb_alt' : len(imgs_alt),
                                                        'category_name' : category,
                                                        'categ_id' : categ_id,
                                                        })

def cart(request):
    response_products = requests.get(f'{url}/products/').json()
    id = request.session.get('id', default=None)
    if id != None :
        products=[]
        mydata = OrderItem.objects.all()
        for item in mydata:
            if item.client_id == id  :
                for product in response_products:
                    if product['id']==item.product_id :
                        products.append(
                                            {
                                                'id' : item.product_id,
                                                'name' : product['name'],
                                                'price' : product['list_price'], 
                                                'image' : product['image_128'], 
                                                'quantity' : item.quantity,
                                                'total' : item.quantity*product['list_price']
                                            }
                                        )
        context = {
            'products' : products
        }
        return render(request, 'shop/shoping-cart.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def checkout(request):
    if request.session.get('id', default=None) == None:
        return HttpResponseRedirect(reverse('login'))
    else :
        url_xmlrpc = 'http://localhost:8069'
        db = 'Marketplace'
        username = 'youneskorbi1999@gmail.com'
        password = '123'
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_xmlrpc))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_xmlrpc))
        mydata = OrderItem.objects.all()
        id = request.session.get('id', default=None)
        response_products = requests.get(f'{url}/products/').json()

        if request.method == 'POST':
            order_data = {
                "state": "sent",
                "date_order": str(datetime.date.today()),
                "user_id": 2,
                "partner_id": 3,
                "partner_invoice_id": 1,
                "partner_shipping_id": 1,
                "picking_policy": "direct",
                "pricelist_id": 1,
                "note": "note",
            }
            order = models.execute(db, uid, password, 'sale.order', 'create', order_data)
            for item in mydata:
                if item.client_id == id :
                    for product in response_products:
                            if product['id']==item.product_id :
                                order_line = models.execute_kw(db, uid, password, 'sale.order', 'write',[[order], {'order_line': [(0, '_', {"product_id": item.product_id, "product_uom_qty": item.quantity})]}],{})
            OrderItem.objects.filter(client_id=id).delete()
            return(redirect('index'))
        else :  
            if id != None :
                products=[]
                for item in mydata:
                    if item.client_id == id :
                        for product in response_products:
                            if product['id']==item.product_id :
                                products.append(
                                                    {
                                                        'id' : item.product_id,
                                                        'name' : product['name'],
                                                        'price' : product['list_price'], 
                                                        'image' : product['image_128'], 
                                                        'quantity' : item.quantity,
                                                        'total' : item.quantity*product['list_price']
                                                    }
                                                )
                context = {
                    'products' : products
                }
            return render(request, 'shop/checkout.html', context)

def products_variant(request, name):
    response_category = requests.get(f'{url}/category/').json()
    response = requests.get(f'{url}/product_variant/{name}').json()
    attributes = requests.get(f'{url}/attribute/').json()
    context = {
        'products': response,
        'attributes' : attributes['Color'],
        'category' : response_category, 
    }
    return render(request, 'shop/shop_variant.html',context)
# ______________________________ CART ______________________________

# Add Item To Cart
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    id = request.session.get('id', default=None)
    try :
        mydata = OrderItem.objects.get(product_id=productId, client_id=id)
        mydata.quantity = mydata.quantity+1
        mydata.save() 
    except:
        data = OrderItem(product_id=productId, client_id=id)
        data.save()

    return JsonResponse('OK', safe=False)

# Delete Cart Item
def delete(request, id):
    item = OrderItem.objects.get(id=id)
    item.delete()
    return HttpResponseRedirect(reverse('cart'))

# Update Cart Quantity Item
    # Update Page
def update(request, id):
    count = 0
    data = OrderItem.objects.all()
    for item in data:
        count = item.quantity + count
    item = OrderItem.objects.get(id=id)
    response = requests.get(f'{url}/products/{str(id)}').json() # Details du produit
    template = loader.get_template('shop/update-cart.html')
    for product in response:
        name = product['name']
        price = product['list_price']
        image = product['image_128']
    context = {
        'name': name,
        'price': price,
        'image': image,
        'id': item.id,
        'quantity' : item.quantity,
        'lenght' : count
    }
    return HttpResponse(template.render(context, request))
    
    # Update Logic
def updaterecord(request, id):
    quantity = request.POST['quantity']
    item = OrderItem.objects.get(id=id)
    item.quantity = quantity
    item.save()
    return HttpResponseRedirect(reverse('cart'))

def getCartLen(request):
    count = 0
    data = OrderItem.objects.all()
    for item in data:
        count = item.quantity + count
    return JsonResponse(count, safe=False)