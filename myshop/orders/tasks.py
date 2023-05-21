from celery import shared_task
from django.core.mail import send_mail
from .models import Order
import os

@shared_task
def order_created(order_id):
    """
    Task to send an email once the order is placed
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have just place an order.\n' \
              f'Your order ID is {order.id}'
    mail_sent = send_mail(subject,
                          message,
                          os.environ.get('EMAIL'),
                          [order.email])
    return mail_sent