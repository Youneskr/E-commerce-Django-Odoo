from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('products/', views.products),
    path('products/<int:id>/', views.product),
    path('category/', views.category),
    path('category/<str:name>/', views.category_details),
    path('sale-order/', views.sale_order),
    path('sale-order-line/<int:id>/', views.sale_order_line),
    path('variante/', views.variante),
    path('attribute/', views.attribute),

    # path('product_template/', views.product_template),
    # path('attribute_id/', views.attribute_id),
    # path('attribute_value/', views.attribute_value),
    path('product_variant/<str:att_name>/', views.product_variant),


    # path('attribute_value/', views.attribute_value),
    path('alternatif/', views.alternative_images),
    path('signup/', views.signup),
]

urlpatterns = format_suffix_patterns(urlpatterns)
