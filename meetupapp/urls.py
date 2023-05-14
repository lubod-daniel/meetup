from django.urls import path
from . import views
from .views import MeetupDelete, UpdateMeetup, CreateMeetup, Loginpage, Register, confirm_registration, user_meetups
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('meetup/<slug:meetup_slug>',views.meetup_details, name='meetup-details'  ),
    path('meetup-delete/<int:pk>', MeetupDelete.as_view(), name='meetup-delete'),
    path('meetup-update/<int:pk>', UpdateMeetup.as_view(), name='meetup-update'),
    path('meetup-create/', CreateMeetup.as_view(), name='meetup_create'),
    path('login/', views.Loginpage, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.Register, name='registration'),
    path('registration-success/', views.confirm_registration, name='confirm-registration'),
    path('add-speakers/<slug:meetup_slug>', views.add_speakers, name='add-speakers'),
    path('user-meetups/<int:pk>',views.user_meetups, name='user-meetups')
    
]