from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .  import views

urlpatterns = [
    path('', views.index, name='home'),
    path('product_list/', views.list_products, name='list_product'),
    path('product_details/<pk>/', views.detail_products, name='detail_products'),
    path('load-data/', views.load_data, name='load_data'),  # ✅ This is what we need
]