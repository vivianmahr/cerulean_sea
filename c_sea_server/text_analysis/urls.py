from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send_JSON', views.send_JSON, name="send_JSON")
]