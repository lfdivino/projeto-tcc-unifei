from django.conf.urls import url
from tcc import views

urlpatterns = [
    url(r'^api/respostas/$', 'tcc.views.respostas', name='respostas'),
    url(r'^api/perguntas/$', 'tcc.views.perguntas', name='perguntas')
]