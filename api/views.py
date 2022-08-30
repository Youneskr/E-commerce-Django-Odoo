from multiprocessing import context
from urllib import response
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import xmlrpc.client


url = 'http://localhost:8069'
db = 'Marketplace'
username = 'youneskorbi1999@gmail.com'
password = '123'
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

'''
    Products API
'''
@api_view(['GET', 'POST'])
def products(request, format=None):
    if request.method == 'GET':
        product_record = models.execute_kw(db, uid, password,'product.product', 'search_read',[[]])
                # , {'fields': ['id', 'name', 'detailed_type', 'list_price']}
        return Response (product_record)
    if  request.method == 'POST':
        models.execute_kw(db, uid, password,'product.product', 'create', [request.data])
        return Response(request.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def product(request, id, format=None):
    if request.method == 'GET':
        product=models.execute_kw(db, uid, password,'product.product', 'search_read',[[['id','=',id]]] )
                # , {'fields': ['id', 'name', 'detailed_type', 'list_price']} 
        if product == []:
            return Response('Produit introuvable', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(product)

    elif  request.method == 'PUT':
        productId = models.execute_kw(db, uid, password,'product.product', 'search', [[]])
        if id in productId:
            models.execute_kw(db, uid, password, 'product.product', 'write', [[id], request.data])
            return Response(request.data)
        else:
            return Response('Produit introuvable', status=status.HTTP_400_BAD_REQUEST)

    elif  request.method == 'DELETE':
        productId = models.execute_kw(db, uid, password,'product.template', 'search', [[]])
        if id in productId:
            models.execute_kw(db, uid, password, 'product.product', 'unlink', [[id]])
            return Response(' is deleted ')
        else:
            return Response('Produit introuvable', status=status.HTTP_400_BAD_REQUEST)

'''
    Category API
'''

@api_view(['GET'])
def category(request):
    if request.method == 'GET':
        product_category = models.execute_kw(db, uid, password,'product.category', 'search_read',[[]])
                # , {'fields': ['id', 'name', 'detailed_type', 'list_price']}
        return Response (product_category)

@api_view(['GET'])
def category_details(request, name):
    if request.method == 'GET':
        details_category = models.execute_kw(db, uid, password,'product.category', 'search_read',[[['name','=',name]]])
        return Response (details_category)

'''
    Variante API
'''

@api_view(['GET'])
def variante(request):
    if request.method == 'GET':
        variante_record = models.execute_kw(db, uid, password,'product.product', 'search_read',[[]])
        return Response (variante_record)

'''
    Alternatif images API
'''
@api_view(['GET'])
def alternative_images(request):
    if request.method == 'GET':
        alternative_images = models.execute_kw(db, uid, password,'product.image', 'create',[[]])
        return Response (alternative_images)

'''
    Login API
'''
@api_view(['POST','GET'])
def signup(request):
    if request.method == 'POST':
        models.execute_kw(db, uid, password,'res.partner', 'create',[request.data])
        return Response('CREATED', status=status.HTTP_201_CREATED)

    elif request.method == 'GET':
        return Response (models.execute_kw(db, uid, password,'res.partner', 'search_read',[[]]))

'''
    Sale Order API
'''
@api_view(['GET','POST'])
def sale_order(request, format=None ):
    if request.method == 'GET':
        return Response(models.execute_kw(db, uid, password,'sale.order', 'search_read',[[]]))

    if request.method == 'POST':
        create_order = models.execute(db, uid, password, 'sale.order', 'create', request.data)
        return Response(create_order, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def sale_order_line(request,id, format=None ):
    if request.method == 'POST':
        create_order_line = models.execute_kw(db, uid, password, 'sale.order', 'write',[[id], {'order_line': [(0, '_', request.data)]}],{})

        return Response('Sale Order Added', status=status.HTTP_201_CREATED)


'''
    Attribute API
'''
@api_view(['GET','POST'])
def attribute(request, format=None ):
    if request.method == 'GET':
        attributes = models.execute_kw(db, uid, password,'product.attribute', 'search_read',[[]])
        values = models.execute_kw(db, uid, password,'product.attribute.value', 'search_read',[[]])
        data = {}

        for attribute in attributes :
            data[attribute['name']] = []

        for attribute in attributes :
            for value in values:
                for id in attribute['value_ids'] :
                    if id == value['id'] :
                        data[attribute['name']].append(value['name'])
        return Response(data)


# @api_view(['GET'])
# def product_template(request, format=None ):
#     if request.method == 'GET':
#         product = models.execute_kw(db, uid, password,'product.template', 'search_read',[[]])
#         return Response(product)

# @api_view(['GET'])
# def attribute_id(request, format=None ):
#     if request.method == 'GET':
#         product = models.execute_kw(db, uid, password,'product.attribute', 'search_read',[[]])
#         return Response(product)

# @api_view(['GET'])
# def attribute_value(request, format=None ):
#     if request.method == 'GET':
#         product = models.execute_kw(db, uid, password,'product.attribute.value', 'search_read',[[]])
#         return Response(product)



@api_view(['GET'])
def product_variant(request,att_name, format=None ):
    if request.method == 'GET':
        att_value = models.execute_kw(db, uid, password,'product.attribute.value', 'search_read',[[]])
        product_template = models.execute_kw(db, uid, password,'product.template', 'search_read',[[]])
        id = []
        for value in att_value :
            if value['name'] == att_name : 
                for line in value['pav_attribute_line_ids'] :
                    for product in product_template :
                        if line in product['attribute_line_ids']:
                            id.append(
                                {
                                    'id' : product['product_variant_id'][0],
                                    'name': product['product_variant_id'][1],
                                    'price' : product['list_price'],
                                    'img': product['image_1920']
                                }
                            )
        if id == [] :
            context = 'NOT FOUND'
        else : 
            context = id
        return Response(context)