from django.shortcuts import render
import requests

url = 'http://127.0.0.1:8000/api'

def index(request):
    response_category = requests.get(f'{url}/category/').json()
    return render (request, 'index.html', {'category' : response_category}) 