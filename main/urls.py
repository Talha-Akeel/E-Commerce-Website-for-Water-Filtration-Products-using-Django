from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('product-list/',views.product_list, name='product-list'),
    path('product-category-list/<int:cat_id>',views.product_category_list, name='product-category-list'),
    path('product-page/',views.product_page, name='product-page'),
    path('product-detail/<str:slug>/<int:id>',views.product_detail, name='product-detail'),
    path('search/',views.search, name='search'),
    path('filter-data',views.filter_data, name='filter_data'),
    path('add-to-cart/',views.add_to_cart, name='add-to-cart'),
    path('cart-page/',views.cart_page, name='cart-page'),
    path('delete-from-cart/',views.delete_from_cart, name='delete-from-cart'),
    path('update-cart/',views.update_cart, name='update-cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/',views.payment_done, name='payment-done'),
    path('payment-cancelled/',views.payment_cancelled, name='payment-cancelled'),
    # User Section Starts
    path('my-dashboard/',views.my_dashboard, name='my-dashboard'),
    path('my-orders/',views.my_orders, name='my-orders'),
    path('my-order-items/<int:id>',views.my_order_items, name='my-order-items'),
    path('my-address-book/',views.my_address_book, name='my-address-book'),
    path('add-address/',views.save_address, name='add-address'),
    path('activate-address/',views.activate_address, name='activate-address'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)