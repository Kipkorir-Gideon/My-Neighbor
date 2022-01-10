from django.test import TestCase
from .models import *
from django.contrib.auth.models import User

# Create your tests here.



class TestProfile(TestCase):
    def setUp(self):
        self.user = User(id=1, username='Ter', password='1234567t')
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()



class TestNeighborhood(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='Ter')
        self.neighborhood = Neighborhood.objects.create(id=1, name='Kikuyu', location='Kiambu', photo='https://cloudinary.com url', neighborhood=self.neighborhood, user=self.user, email='Ter@Ter.com')

    def test_create_neighborhood(self):
        self.neighborhood.create_neighborhood()
        neighborhood = Neighborhood.objects.all()
        self.assertTrue(len(neighborhood) >0)

    def test_find_neighborhood(self, id):
        self.neighborhood.save()
        neighborhood = Neighborhood.find_neighborhood(neighborhood_id = id)
        self.assertTrue(len(neighborhood) == 1)



class TestBusiness(TestCase):
    def setUp(self):
        self.user = User.objects.create(id = 1, username='Ter')
        self.neighborhood = Neighborhood.objects.create(id=1, name='Kikuyu')
        self.business = Business.objects.create(id=1, name='Cyber', description='Computer services', photo='https://cloudinary.com url', neighborhood_d=self.neighborhood, owner=self.user, email='Ter@Ter.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.business, Business))

    def test_create_business(self):
        self.business.save_business()
        business = Business.objects.all()
        self.assertTrue(len(business) > 0)

    def test_find_business(self, word):
        self.business.save()
        business = Business.search_by_business_name(search_term=word)
        self.assertTrue(len(business) == 1)



class TestPost(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='Ter')
        self.neighborhood = Neighborhood.objects.create(id=1, name='Kikuyu')
        self.post = Post.objects.create(id=1, title='Holiday', description='Happy holidays everyone', photo='https://cloudinary.com url', neighborhood=self.neighborhood, user=self.user, date_posted='2022,1,10')

    def test_instance(self):
        self.assertTrue(isinstance(self.post, Post))

    def test_save_post(self):
        self.post.save_post()
        posts = Post.objects.all()
        self.assertTrue(len(posts) > 0)

    def test_delete_post(self):
        self.post.delete_post()
        posts = Post.objects.all()
        self.assertTrue(len(posts) == 0)

    def test_show_post(self):
        self.post.save()
        posts = Post.show_posts()
        self.assertTrue(len(posts) > 0)