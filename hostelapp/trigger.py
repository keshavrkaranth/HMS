from twilio.rest import Client
from django.dispatch import receiver
from .models import *
from django.db.models.signals import post_save





#
#
twilio_sid = 'ACe5540840f09d2c2fc9cabaa750c8d0e3'
twilio_api = 'a0206af2ecdedbc0ebcbec894e7ec95e'
twilio_phno = '(938) 300-4223'


client = Client(twilio_sid, twilio_api)

@receiver(post_save,sender=Student)
def student_after_reg(sender,instance,created,**kwargs):
    if not created:
        if not instance.room_allotted:
            msg = f'''Dear {instance.student_name} You have registerd sucessfully for Canara Hostel Services Enjoy Your Hostel Life:) '''
            message = client.messages \
                .create(
                body=msg,
                from_=twilio_phno,
                to=f'+91{instance.student_mbl_no}'
            )
        elif instance.room_allotted :
            msg = f''' Dear {instance.student_name} Your room type {instance.room.room_type} and room number is {instance.room.no} ThankYou for availing our services'''
            client.messages \
                .create(
                body = msg,
                from_=twilio_phno,
                to=f'+91{instance.student_mbl_no}'
            )

@receiver(post_save,sender=Leave)
def leave(sender,instance,created,**kwargs):
    if created:
        obj = instance.student.room.hostel
        usr = Warden.objects.get(hostel = obj)
        wardenmsg = f''' Hello {usr}. {instance.student.student_name} have applied for leave please go and look after it'''
        stumsg = f''' You have applied for  leave please wait till it accepts/rejects'''
        parentmsg = f''' Dear Sir/madam Your son/Daughter applied for leave from {instance.start_date}-{instance.end_date} '''
        client.messages \
            .create(
            body=wardenmsg,
            from_=twilio_phno,
            to=f'+91{usr.phoneno}'
        )
        client.messages \
            .create(
            body=stumsg,
            from_=twilio_phno,
            to=f'+91{instance.student.student_mbl_no}'
        )
        client.messages \
            .create(
            body=parentmsg,
            from_=twilio_phno,
            to=f'+91{instance.student.father_mbl_no}'
        )


