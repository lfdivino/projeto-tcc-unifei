from django.conf.urls import url
from tcc import views

urlpatterns = [
    url(r'^respostateste/$', views.respostateste),
]