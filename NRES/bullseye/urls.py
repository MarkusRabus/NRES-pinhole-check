from django.conf.urls import url

from . import views

app_name = "bullseye"

urlpatterns = [
    url(r'^$', views.guider_images, name='guider_images'),
]