from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



urlpatterns =[
    path('',views.neighborhood,name='neighborhood'),
    path('register/', views.register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate_account, name='activate'),
    path('accounts/login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('join_neighborhood/<int:neighborhood_id>', views.join_hood, name='join_neighborhood'),
    path('my_neighborhood/<int:neighborhood_id>/', views.my_neighborhood, name='my_neighborhood'),
    path('leave_neighborhood/<int:neighborhood_id>', views.leave_hood, name='leave_neighborhood'),
    path('search',views.search, name='search'),

]

if settings.DEBUG:

    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)