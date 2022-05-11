from . import views
from django.urls import path


urlpatterns = [
    path('',views.storeview,name='store'),
    path('cart/',views.cartview,name='cart'),
    path('checkout/',views.checkoutview,name='checkout'),
    path('update_item/',views.updateitem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),

]