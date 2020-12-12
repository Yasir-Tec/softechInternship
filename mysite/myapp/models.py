from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

def only_int(value):
    if value.isdigit() == False:
        raise ValidationError('Mobile-Number contains Characters.(Number must be in +91(your Mobile Number) Formats')

def only_char(value):
    if value.isdigit()==True:
        raise ValidationError('Name must be in STRING Format (Contains only characters ,Avoid any digits,symbols,emojis)')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, default='o')
    last_name = models.CharField(max_length=100, blank=True, default='o')
    email = models.EmailField(max_length=150, default='Email not found', unique=True)
    mobile = models.CharField(max_length=15, default='j')
    is_active = models.BooleanField(default=False)
    username = models.CharField(max_length=200, default='a')
    password = models.CharField(max_length=200, default='z')
    otp = models.CharField(max_length=6, default='j')
    image = models.ImageField(upload_to="photos/", max_length=2559, default='default.jpg')
    CompanyID = models.CharField(max_length=20, default='a')
    Activate_Account = models.BooleanField(default=False)




    @property
    def image_url(self):
        try:
            img = open(self.image.path, "rb")
            data = img.read()
            return "data:image/jpg;base64,%s" % data.encode('base64')

        except IOError:
            return self.image.url

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class photo(models.Model):
    image = models.ImageField(upload_to="photos/", max_length=2559)
    username = models.CharField(max_length=200, default='a')

    @property
    def image_url(self):
        try:
            img = open(self.image.path, "rb")
            data = img.read()
            return "data:image/jpg;base64,%s" % data.encode('base64')

        except IOError:
            return self.image.url
