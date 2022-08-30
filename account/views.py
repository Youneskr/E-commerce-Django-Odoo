from shutil import register_unpack_format
from django.shortcuts import render, redirect
import requests
from django.contrib import messages

login_url ='http://127.0.0.1:8069/api/login'
signup_url ='http://127.0.0.1:8000/api/signup'
db = 'Marketplace'

def myaccount(request):
    return render(request, 'account/myaccount.html')

def account(request):
    return render (request, 'account/account.html')

def sign_up_user(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        new_user = {
            "name": fname,
            "phone": phone,
            "email":email
        }
    else :
        return render(request, 'account/signup.html')

def login_user(request):
    if request.method == 'POST':

        login = request.POST['email']
        password = request.POST['password']

        headers = {'login': login, 'password': password, 'db': db}
        data = requests.get(login_url, headers=headers)

        if data.status_code == 200 :
            request.session['email'] = login
            request.session['name'] = data.json()['name']
            request.session['id'] = data.json()['uid']
            request.session['image'] = data.json()['image']
            return redirect('index')
        else:
            return redirect('login')
    else:
        if request.session.get('id', default=None) != None  :
            return redirect('index')
        return render(request, 'account/login.html')

def logout_user(request):
    del request.session['email']
    del request.session['name']
    del request.session['id']
    del request.session['image']
    return redirect('index')