from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^submit_form/', views.submit_form, name='submit_form'),
    url(r'^submit_form_html/', views.submit_form_html, name='submit_form_html'),
    url(r'^log_out/', views.log_out, name='log_out'),
    url(r'^home/', views.home, name='home'),
    url(r'^voc/', views.voc, name='voc'),
    url(r'^record/', views.record, name='record'),
    url(r'^stats/', views.stats, name='stats'),
    url(r'^quizz/', views.quizz, name='quizz'),
    #url(r'^exe/', views.exe, name='exe'),
    ]

if settings.DEBUG:
   import debug_toolbar
   urlpatterns = [
       url(r'^__debug__/', include(debug_toolbar.urls)),
   ] + urlpatterns