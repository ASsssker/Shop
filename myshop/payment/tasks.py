from io import BytesIO
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
import os
import weasyprint


@shared_task
def payment_complete(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'My shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         settings.EMAIL,
                         [order.email])
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    email.attach(f'order_{order_id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    email.send()