from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .  import views

urlpatterns=[
    path('cart',views.show_cart,name='cart'),
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('remove_item/<int:pk>/', views.remove_from_cart, name='remove_item'),
    path('payment/', views.start_payment, name='start_payment'),
    path('checkout', views.checkout_cart, name='checkout'),
    path('orders/', views.view_orders, name='orders'),
    path('orders/<int:order_id>/track/', views.track_order, name='track_order'),
    path('orders/<int:order_id>/invoice/', views.download_invoice, name='download_invoice'),
    path('cart/save-address/', views.save_address, name='save_address'),



]