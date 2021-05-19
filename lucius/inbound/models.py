from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# Inventing is what makes me happy... 

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
    emergency_msg = models.CharField(max_length=255)

    # kitestring calls this 'Perennial mode'
    continual_monitoring = models.BooleanField(default=False)

    last_check_in = models.DateTimeField(null=True)
    checked_in_until = models.DateTimeField(null=True)
    emergency_started = models.DateTimeField(null=True)

# A user has multiple contacts.
# Contact has a name and number and an emergency bit
class Contact(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    emergency_contact = models.BooleanField(default=True)

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

