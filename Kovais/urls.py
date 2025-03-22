from django.urls import path
from .views import *

# from .views import video_processing_view

urlpatterns = [
    # customers
    path('create-customer/', create_user_details),
    path('customer-login/', customer_login),
    path('total-users/', AsyncUserList.as_view()),
    path('orders/',orders_by_user_id),
    path('post-review/', submit_review),

    # employees
    
    # path('Employee-login/', Emp_login, name='employee_login'),
    path('create-employee/', create_Employee, name='create_employee'),
    path('total-employees/', total_employees, name='total_employees'),
    path('update-employee/', update_employee, name='update_employee'),
    path('delete-employee/', delete_employee, name='delete_employee'),

    path('get_order_by_id_and_date/', get_order_by_id_and_date, name ="get order by employee id and date"),

    # saloon
    path('get/saloon/orders/', get_saloon_orders),
    path('saloon/orders/', post_saloon_orders),
    path('filter_saloon_order_by_status/<int:user_id>', filter_by_status_and_user, name="filter saloon order by user and status"),
    path('saloon/update/', update_saloon_orders),
    path('filter_saloon_order_by_status/', get_saloon_order_status, name="filter spa order by status"),
    path('filter_saloon_order_by_payment_status/', get_saloon_payment_status, name="filter hotel order by user and status"),
    # gym
    path('get/gym/orders/', get_gym_orders),
    path('gym/update/', update_gym_orders),
    path('gym/orders/', post_gym_orders),
    path('filter_gym_order_by_status/', get_gym_order_status, name="filter spa order by status"),
    path('filter_gym_order_by_payment_status/', get_gym_payment_status, name="filter hotel order by user and status"),

    # spa
    path('get/spa/orders/', get_spa_orders),
    path('spa/orders/', post_spa_orders),
    path('spa/update/', update_spa_orders),
    path('filter_spa_order_by_status/', get_spa_order_status, name="filter spa order by status"),
    path('filter_spa_order_by_payment_status/', get_spa_payment_status, name="filter hotel order by user and status"),


    # hotel
    path('get/hotel/orders/', get_hotel_orders),
    path('hotel/orders/', post_hotel_orders),
    path('hotel/update/', update_hotel_orders),
    path('filter_hotel_order_by_status/', get_hotel_order_status, name="filter hotel order by user and status"),
    path('filter_hotel_order_by_payment_status/', get_payment_status, name="filter hotel order by user and status"),
    path('orders/', get_hotel_orders),
    path('room-count/', get_room_count),

    # Attendance
    path('Attendance/', create_attendance),
    path('get-attendance-id/', get_attendance_id),
    path('get/all-attendance/', get_all_attendance),
    path('get-present/', get_present),

    # Admin task manager

    path('create-task/', create_task),
    path('get-all-tasks/', get_all_task),
    path('update-task/', update_task),
]
