from django.contrib import admin
from django.urls import path, include
from django.conf.urls import(handler400,handler403,handler404,handler500)

handler500 = 'polls.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
]
