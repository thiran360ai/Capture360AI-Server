from django.urls import path

from .views import *

# from .views import video_processing_view

urlpatterns = [
    #customers
    path('create-customer/',create_user_details),
    path('customer-login/',Customer_login),
    path('total-users/',users),

    #employees
    path('Employee-login/', Emp_login),
    path('create-employee/', create_Employee, name='create_user'),
    path('total-employees/', total_employees, name='total_users'),

    # saloon

    path('get/saloon/orders/',get_saloon_orders),
    path('saloon/orders/',post_saloon_orders),

    #gym
    path('get/gym/orders/',get_gym_orders),
    path('gym/orders/',post_gym_orders),


    #spa
    path('get/spa/orders/',get_spa_orders),
    path('spa/orders/',post_spa_orders),


    #hotel
    path('get/hotel/orders/',get_hotel_orders),
    path('hotel/orders/',post_hotel_orders),

    path('filter_saloon_order_by_status/<int:user_id>',filter_by_status_and_user,name="filter saloon order by user and status")
]
