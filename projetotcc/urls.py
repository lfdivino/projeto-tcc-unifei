from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from tcc import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'perguntas', views.PerguntaViewSet)


urlpatterns = [
        url(r'^', include('tcc.urls')),
    url(r'^$', 'tcc.views.home', name='home'),
    # url(r'^configuracao/$', 'tcc.views.configuracao', name='configuracao'),
    # url(r'^contato/$', 'tcc.views.contato', name='contato'),
    url(r'^admin/analise/$', views.analise_dados),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)