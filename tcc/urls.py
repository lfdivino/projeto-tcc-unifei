from django.conf.urls import url

urlpatterns = [
    url(r'^api/respostas/$', 'tcc.views.respostas', name='respostas'),
    url(r'^api/respostas/(?P<question_id>[0-9]+)/$', 'tcc.views.respostas', name='respostas'),
    url(r'^api/perguntas/$', 'tcc.views.perguntas', name='perguntas')

]