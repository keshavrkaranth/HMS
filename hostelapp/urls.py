from django.urls import path
from .views import *


app_name = 'hostelapp'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('signup/', user_registration, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('student_profile/', student_profile, name='student_profile'),
    path('room_maintenence/', maintainence, name='room_maintenence'),
    path('warden_home/', warden_homepage, name='warden_home'),
    path('leave/', user_leave, name='leave'),
    path('get_room/', get_room, name='get_room'),
    path('select_room/<int:pk>/', select_room, name='select_room'),
    path('addroom/',Warden_add_room,name='addroom'),
    path('leaveapplications/',leave_applications,name='leaveapplications'),
    path('acceptleave/<int:pk>/',accept_leave,name='acceptleave'),
    path('rejectleave/<int:pk>/',reject_leave,name='rejectleave'),
    path('roomgrivelences/',wardenroom_grivelences,name='roomgrivelences'),
    path('resolve/<int:pk>/',warden_resolve,name='resolve'),
    path('feedback/',feedback,name='feedback'),
    path('feedback_home',feedback_home,name='feedback_home'),
]
