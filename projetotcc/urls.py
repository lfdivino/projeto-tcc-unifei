from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'tcc.views.home', name='home'),
    # url(r'^configuracao/$', 'tcc.views.configuracao', name='configuracao'),
    # url(r'^contato/$', 'tcc.views.contato', name='contato'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
