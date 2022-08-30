from django.urls import path
from . import views

urlpatterns = [
    path('',views.shop_page, name='shop'),
    path('count/',views.getCartLen, name='getCartLen'),
    path('update_item/',views.updateItem, name='updateItem'),
    path('shoping-cart/',views.cart, name='cart'),
    path('shoping-cart/update/<int:id>', views.update, name='update'),
    path('filter-<str:name>/', views.products_variant, name='products_variant'),
    path('shoping-cart/update/updaterecord/<int:id>', views.updaterecord, name='updaterecord'),
    path('checkout/',views.checkout, name='checkout'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('<int:id>/',views.details, name='details'),
    path('<str:category>/',views.category, name='category'),
]
