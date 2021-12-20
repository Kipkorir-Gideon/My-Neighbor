from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = CloudinaryField(blank=True, default = 'profile photo')
    bio = models.TextField()
    email = models.EmailField()
    neighborhood = models.ForeignKey('Neighborhood', on_delete=models.CASCADE)

    #Creates a profile when a user is created
    @receiver(post_save, sender = User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    #Saves the User's profile information
    @receiver(post_save, sender = User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_user_profile(self):
        self.save()

    def delete_user_profile(self):
        self.delete()

    def __str__(self):
        return "%s profile" % self.user



class Neighborhood(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    people = models.IntegerField()
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE)
    police_info = models.IntegerField()
    hospital_info = models.IntegerField()