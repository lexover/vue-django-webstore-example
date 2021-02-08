from django.core.mail import send_mail
from drugstore.celery import app
from django.template.loader import render_to_string


@app.task
def send_order_acceptance(data):
    message = f'Thanks for your choice!\n' \
              f'Your order # {data["id"]} will be delivered soon.'\
              f'Total: {data["total"]}'
    html_message = render_to_string('email_template_order.html', data)
    send_mail(
        message=message,
        subject=f'Order #{data["id"]} confirmation',
        from_email='lexover@ya.ru',
        recipient_list=[data['email']],
        html_message=html_message,
        fail_silently=False
    )
