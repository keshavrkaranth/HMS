from twilio.rest import Client
from django.dispatch import receiver
from .models import *
from django.db.models.signals import post_save
from decouple import config



@receiver(post_save,sender=User)
def username_changer(sender,instance,created,**kwargs):
    if created:
        tmp = User.objects.get(username=instance.username)
        if tmp.username != tmp.username.upper():
            tmp.username = tmp.username.upper()
            tmp.save()
        else:
            pass


@receiver(post_save,sender=Student)
def student_after_reg(sender,instance,created,**kwargs):
    client = Client(config('twilio_sid'), config('twilio_api'))
    if not created:
        if not instance.room_allotted:
            msg = f'''Dear {instance.student_name} You have registerd sucessfully for Canara Hostel Services Enjoy Your Hostel Life:) '''
            message = client.messages \
                .create(
                body=msg,
                from_=config('twilio_phno'),
                to=f'+91{instance.student_mbl_no}'
            )
        else:
            msg = f''' Dear {instance.student_name} Your room type {instance.room.room_type} and room number is {instance.room.no} ThankYou for availing our services'''
            client.messages \
                .create(
                body = msg,
                from_=config('twilio_phno'),
                to=f'+91{instance.student_mbl_no}'
            )

