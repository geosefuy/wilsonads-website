from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer
from django.dispatch import receiver

@receiver (post_save, sender=User)
def create_customer (sender, instance, created, **kwargs):
	if created:
		Customer.objects.create(user=instance, fname=instance.first_name, lname=instance.last_name, email=instance.email)
		
		