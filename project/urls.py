from django.contrib import admin
from django.urls import path, include
from . import views
from account.views import logout_user, sign_up_user

urlpatterns = [
    path('',views.index, name='index'),
    path('shop/',include('shop.urls')),
    path('api/',include('api.urls')),
    path('user/',include('account.urls')),
    path('logout/',logout_user, name='logout'),
    path('signup/',sign_up_user, name='sign_up_user'),
    path('admin/', admin.site.urls, name='admin'),
]
