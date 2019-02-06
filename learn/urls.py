from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^voc/', views.voc, name='voc'),
    url(r'^record/', views.record, name='record'),
    ]

if settings.DEBUG:
   import debug_toolbar
   urlpatterns = [
       url(r'^__debug__/', include(debug_toolbar.urls)),
   ] + urlpatterns