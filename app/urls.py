from django.urls import path
# from .views import register_user, register_employee, category_list_create, profile_list_create, product_list_create, order_list_create
from .views import*
from django.urls import re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/user/', register_user, name='register'),
    path('register/employee/', register_employee, name='register_employee'),
    path('categories/', category_list_create, name='categories'),
    # path('profiles/', profile_list_create, name='profiles'),
    # path('products/', product_list_create, name='products'),
    path('profiles/', profile_list_create, name='profile-list-create'),

    # Product URLs
    path('products/', product_list_create, name='product-list-create'),

    # Product Variation URLs
    path('product-variations/', product_variation_list_create, name='product-variation-list-create'),




    path('orders/', order_list_create, name='orders'),
    path('search/', search_nearest_products, name='search_nearest_products'),
    path('login/', login_user, name='login'),

    re_path(r'ws/order/(?P<order_id>\d+)/$', OrderTrackingConsumer.as_asgi()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login (Generate Token)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
]



