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
    location = models.CharField(max_length=50, blank=True, null=True)

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
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='admin')
    police_info = models.IntegerField()
    hospital_info = models.IntegerField()
    photo = CloudinaryField(blank=True, default = 'photo')

    def create_neighborhood(self):
        self.save()

    def delete_neighborhood(self):
        self.delete()

    @classmethod
    def find_neighborhood(cls, neighborhood_id):
        return cls.objects.filter(id=neighborhood_id)

    def __str__(self):
        return "%s neighborhood" % self.name




class Business(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    neighborhood_id = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    email = models.EmailField()

    def save_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    @classmethod
    def search_by_business_name(cls, search_term):
        business = cls.objects.filter(name__icontains=search_term)
        return business

    def __str__(self):
        return "%s business" % self.name



class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    
            
    class Meta:
        ordering = ['-date_posted']
    
    def save_post(self):
        self.save()

    def __str__(self):
        return self.title