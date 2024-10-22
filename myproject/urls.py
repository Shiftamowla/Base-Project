from django.contrib import admin
from django.urls import path
from myproject.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    path('deletejob/<int:id>', deletejob, name='deletejob'),
    path('mainprofile/<int:id>', mainprofile, name='mainprofile'),
    path('editjob/<int:id>', editjob, name='editjob'),
    path('Addjob/', Addjob, name='Addjob'),
    path('jobfeed/', jobfeed, name='jobfeed'),


    path('searchJob/', searchJob, name='searchJob'),
    path('appliedJob/', appliedJob, name='appliedJob'),
    path('ApplyNow/<str:job_title>/<int:id>', ApplyNow, name='ApplyNow'),
    path('Table/', Table, name='Table'),
    path('base/', base, name='base'),


    path('addSkill/', addSkill, name='addSkill'),
    path('editSkill/<int:id>', editSkill, name='editSkill'),
    path('skilldeletepage/<int:id>', skilldeletepage, name='skilldeletepage'),

    path('Profile/', Profile, name='Profile'),
    path('updateprofile/<int:id>', updateprofile, name='updateprofile'),

    path('', loginpage, name='loginpage'),
    path('password_change', password_change, name='password_change'),
    path('registerpage/', registerpage, name='registerpage'),
    path('logoutpage/', logoutpage, name='logoutpage'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
