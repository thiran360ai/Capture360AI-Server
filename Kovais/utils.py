from .models import *
from asgiref.sync import sync_to_async

async def get_orders_from_db():
    
    from .models import HotelOrder 
    orders = await sync_to_async(list)(HotelOrder.objects.aall()) 
    return orders


async def aget_available_room_count():
    from .models import Rooms 
    room= await sync_to_async(Rooms.objects.afilter(status='Available').count)()
    return room