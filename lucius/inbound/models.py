from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# A user has a name, account ID, and a pin.
class Profile(models.Model):
    class Plan(models.IntegerChoices):
        FREE = 1
        BRONZE = 2
        GOLD = 3
        PLATINUM = 4

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.IntegerField(choices=Plan.choices, default=1)

    pin = models.CharField(max_length=10)
    duress_code = models.CharField(max_length=10)

    in_emergency = models.BooleanField(default=False)
    emergency_msg = models.CharField(max_length=4096, default='I am in trouble and I need assistance. Please contact me ASAP.')

    # kitestring calls this 'Perennial mode'
    continual_monitoring = models.BooleanField(default=False)
    check_interval = models.IntegerField(default=4 * 60)

    last_check_in = models.DateTimeField(null=True, blank=True)
    checked_in_until = models.DateTimeField(null=True, blank=True)
    emergency_started = models.DateTimeField(null=True, blank=True)

    message_sid = models.CharField(max_length=255, null=True, blank=True)
    message_url = models.CharField(max_length=255, null=True, blank=True)
    message_transcribe = models.CharField(max_length=2048, null=True, blank=True)

# A user has multiple contacts.
# A Contact has a name and number and an emergency bit and some details
# about how to contact them.
class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    sms_capable = models.BooleanField(default=True)

    # if true, we'll call you when the user is in emergency.
    emergency_contact = models.BooleanField(default=True)
    last_voice = models.DateTimeField(null=True, blank=True)
    last_sms = models.DateTimeField(null=True, blank=True)
    # an acknowledgement of any kind will stop the contact train.
    last_ack = models.DateTimeField(null=True, blank=True)
    retry_interval = models.IntegerField(default=60) # minutes
    
# handle save/create signals to extend profile
@receiver(post_save, sender=User) 
def create_user_profile(sender, instance, created, **kwargs):
     if created:
         Profile.objects.create(user=instance)

@receiver(post_save, sender=User) 
def save_user_profile(sender, instance, **kwargs):
     instance.profile.save()

# An incident / emergency is a single thing
# it has a contact record.

