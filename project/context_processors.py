from shop.models import OrderItem
import requests

def global_context(request):
    context = {}
    url = 'http://127.0.0.1:8000/api'
    # Sessions Login
    context['email'] = request.session.get('email', default=None)
    context['username'] = request.session.get('name', default=None)
    context['uid'] = request.session.get('id', default=None)
    context['user_image'] = request.session.get('image', default=None)

    # Number of Cart Items & Total
    data = OrderItem.objects.all()
    count = 0
    total_cart = 0
    for item in data:
        if item.client_id == context['uid'] :
            response_product = requests.get(f'{url}/products/{str(item.product_id)}').json()
            count = item.quantity + count
            total_cart = total_cart + (item.quantity * response_product[0]['list_price'])

    context['lenght'] = count
    context['total_cart'] = total_cart
    return context