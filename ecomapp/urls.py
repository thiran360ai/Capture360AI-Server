from django.urls import path
from .views import *

urlpatterns = [
    path("register/user/",register_user, name="Users-Register"),
    # path("register/shopkeeper/", register_shopkeeper, name="shopkeeper-register"),
    path("login/", login_user , name="login"),
    path("logout/", logout_user, name="logout"),
    path("Banners/",manage_banners,name="Banners-Shopkeeper"),
    path("token/refresh/",refresh_token,name="refresh-token"),
    path('categories/', manage_categories, name='manage_categories'),
    path('subcategories/', manage_subcategories, name='manage_subcategories'),
    path('profiles/', profile_list_create, name='shopkeeper-list-create'),
    # path('profiles/<int:pk>/', profile_detail, name='shopkeeper-detail'),

    #Products APIs
    path('products/<int:product_id>/upload-images/', upload_product_images, name='upload_product_images'),
    path('products/<int:product_id>/images/', get_product_images, name='get_product_images'),
    # path('products/images/<int:image_id>/delete/', delete_product_image, name='delete_product_image'),
    path('products/', product_list_create, name='product-list-create'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
    path('products/<int:product_id>/variations/', product_variation_list_create, name='product-variation-list-create'),
    path('search-product/', search_product, name='search-product'),

    # Cart APIs
    path('cart/', get_cart, name='get-cart'),
    path('cart/add/', add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove-from-cart'),
    path('cart/clear/', clear_cart, name='clear-cart'),

    # Orders APIs
    path('order-from-cart/', order_from_cart, name='order_from_cart'),
    path('place-order-direct/', place_order_direct, name='place_order_direct'),
    path('orders/<int:order_id>/', get_order_details, name='get-order-details'),  # GET Order Details
    path('orders/<int:order_id>/accept/', accept_order, name='accept-order'),  # Shopkeeper Accept Order

    # Wishlist APIs
    path('wishlist/add/', add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/', get_wishlist, name='get-wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove-from-wishlist'),

    # Review APIs
    path('reviews/add/', add_review, name='add-review'),
    path('reviews/<int:product_id>/', get_product_reviews, name='get-product-reviews'),
    path('reviews/update/<int:review_id>/', update_review, name='update-review'),
    path('reviews/delete/<int:review_id>/', delete_review, name='delete-review'),

    # Address APIs
    path('addresses/add/', add_address, name='add-address'),
    path('addresses/', get_addresses, name='get-addresses'),
    path('addresses/update/<int:address_id>/', update_address, name='update-address'),
    path('addresses/delete/<int:address_id>/', delete_address, name='delete-address'),

     # Payment APIs
    path('payments/create/', create_payment, name='create-payment'),
    path('payments/', get_payments, name='get-payments'),
    path('payments/update/<int:payment_id>/', update_payment, name='update-payment'),
    path('payments/delete/<int:payment_id>/', delete_payment, name='delete-payment'),

    # Delivery Partner APIs
    path('delivery-partners/add/', add_delivery_partner, name='add-delivery-partner'),
    path('delivery-partners/', get_delivery_partners, name='get-delivery-partners'),
    path('delivery-partners/update/<int:partner_id>/', update_delivery_partner, name='update-delivery-partner'),
    path('delivery-partners/delete/<int:partner_id>/', delete_delivery_partner, name='delete-delivery-partner'),

    # Order Tracking APIs
    path('tracking/add/', add_order_tracking, name='add-order-tracking'),
    path('tracking/<int:order_id>/', get_order_tracking, name='get-order-tracking'),
    path('tracking/update/<int:tracking_id>/', update_order_tracking, name='update-order-tracking'),
    path('tracking/delete/<int:tracking_id>/', delete_order_tracking, name='delete-order-tracking'),

    # Notification APIs
    path('notifications/create/', create_notification, name='create-notification'),
    path('notifications/', get_notifications, name='get-notifications'),
    path('notifications/read/<int:notification_id>/', mark_notification_read, name='mark-notification-read'),
    path('notifications/delete/<int:notification_id>/', delete_notification, name='delete-notification'),
    path('search/', search_productss, name='related search_products'),



]
