from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('categories/', views.bikeView.as_view(), name='category-create'),
    path('categories/<int:id>/', views.bikeViewById.as_view(), name='category-detail'),
    
    path('products/', views.ProductListView.as_view(), name='product-list-create'),
    path('products/<int:id>/', views.productlistViewById.as_view(), name='product-detail'),
    
    path('accessories/', views.accesoriesView.as_view(), name='accessory-list-create'),
    path('accessories/<int:id>/', views.accesoriesViewById.as_view(), name='accessory-detail'),
    
    path('banners/', views.BannerListCreate.as_view(), name='banner-list-create'),
    path('banners/<int:id>/', views.BannerDetail.as_view(), name='banner-detail'),
    
    path('items/', itemsView.as_view(), name='items-list-create'),
    path('items/<int:id>/', itemsViewById.as_view(), name='items-detail'),
    path('Wish/send_email/', SendWishEmailView.as_view(), name='send_wishlist_email'),

    path('Wish/', WishListView.as_view(), name='Wish-view'),
    path('Wish/add/', AddToWishView.as_view(), name='wish-add'),
    path('Wish/update/<int:wish_id>/', UpdateWishView.as_view(), name='update-Wish'),
    path('Wish/remove/<int:wish_id>/', RemoveWishItemView.as_view(), name='remove-item'),
    
    path('customers/', CustomerListCreateView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    
    path('contact/',contactView.as_view(),name='contact-detail'),
    
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('register-user/', UserSignupView.as_view(), name='register-user'),
    path('register-admin/', AdminSignupView.as_view(), name='register-admin'),   
    
    # path('order/create/', CreateOrderView.as_view(), name='create_order'),
    path('order/list/', OrderListView.as_view(), name='order_list'),
]