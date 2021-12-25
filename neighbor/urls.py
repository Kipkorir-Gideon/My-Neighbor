from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



urlpatterns =[
    path('',views.neighborhood,name='neighborhood'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/<pk>', views.profile, name='profile'),

]

if settings.DEBUG:

    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)