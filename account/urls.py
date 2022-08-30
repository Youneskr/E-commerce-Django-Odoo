from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('myaccount/', views.myaccount , name='account'),
    path('account/', views.account),
]
