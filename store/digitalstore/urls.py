from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='main'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product'),
    path('category/<slug:slug>/', ProductByCategory.as_view(), name='category'),
    path('login/', login_user_view, name='login'),
    path('logout/', logout_user_view, name='logout'),
    path('registration/', register_view, name='register'),
    path('save_favorite/<slug:slug>/', save_favorite_product, name='save_favorite'),
    path('favorites/', FavoriteListView.as_view(), name='favorites'),
    path('add_or_delete/<slug:slug>/<str:action>/', add_or_delete_product_view, name='add_or_del'),
    path('my_cart/', my_cart_view, name='my_cart'),
    path('delete/<int:pk>/<int:order_id>/', delete_product, name='delete'),
    path('checkout/', checkout_view, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success/', success_payment, name='success'),
    path('search/', SearchProduct.as_view(), name='search'),
    path('profile/', profile_view, name='profile'),
    path('orders/', orders_list, name='orders_list'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
]

















