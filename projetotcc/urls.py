from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from tcc import views


urlpatterns = [
    url(r'^', include('tcc.urls')),
    url(r'^$', 'tcc.views.home', name='home'),
    # url(r'^configuracao/$', 'tcc.views.configuracao', name='configuracao'),
    # url(r'^contato/$', 'tcc.views.contato', name='contato'),
    url(r'^admin/analise/$', views.analise_dados),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)