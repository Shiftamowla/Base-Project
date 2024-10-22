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
    path('addSkill/', addSkill, name='addSkill'),
    path('editSkill/<int:id>', editSkill, name='editSkill'),
    path('skilldeletepage/<int:id>', skilldeletepage, name='skilldeletepage'),
    path('Table/', Table, name='Table'),
    path('jobfeed/', jobfeed, name='jobfeed'),
    path('searchJob/', searchJob, name='searchJob'),
    path('appliedjob/', appliedjob, name='appliedjob'),
    path('base/', base, name='base'),
    path('', loginpage, name='loginpage'),
    path('password_change', password_change, name='password_change'),
    path('registerpage/', registerpage, name='registerpage'),
    path('logoutpage/', logoutpage, name='logoutpage'),
    path('Profile/', Profile, name='Profile'),
    path('updateprofile/<int:id>', updateprofile, name='updateprofile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
