from celery import shared_task
from .models import Order  # Import only models at the top

@shared_task
def assign_order(order_id):
    from .views import send_order_update  # Import inside function to avoid circular import

    order = Order.objects.get(id=order_id)
    if order.status == 'Pending':
        order.status = 'Forwarded'
        order.save()
        send_order_update(order.id, "Forwarded to next shop")
