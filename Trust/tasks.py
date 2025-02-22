from celery import shared_task
import pywhatkit as kit
from .models import Contact

@shared_task
def send_whatsapp_task(phone_number):
    try:
        # Fetch contact details
        order = Contact.objects.get(mobile=phone_number)
        payee_name = order.name
        amount = order.payment

        # Message Content
        message = f"""Hi {payee_name},

            Just wanted to let you know that the payment of {amount} has been successfully made to your account. 
            
            Please check and confirm when convenient.

            Thank you for your continued trust and partnership — it’s truly appreciated!

            Best regards,
            DRUKEN MONKEY
            chennai-600077"""

        # Defaults: wait_time=10, close_time=5
        kit.sendwhatmsg_instantly(phone_number, message, 10, True, 5)

        return "WhatsApp message sent successfully!"
    except Contact.DoesNotExist:
        return "Contact not found."
    except Exception as e:
        return str(e)
