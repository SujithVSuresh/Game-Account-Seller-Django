from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#            subject = 'welcome to GFG world'
#            message = render_to_string('accounts/acc_active_email.txt', {
#					"email":instance.email,
#					'domain':'127.0.0.1:8000',
#					'site_name': 'Website',
#					"uid": urlsafe_base64_encode(force_bytes(instance.pk)),
#					"user": instance,
#					'token': default_token_generator.make_token(instance),
#					'protocol': 'http',
#            })
            #message = f'Hi {instance.username}, thank you for registering in geeksforgeeks.'
#            email_from = settings.EMAIL_HOST_USER
#            recipient_list = [instance.email, ]
#            send_mail( subject, message, email_from, recipient_list )

        
