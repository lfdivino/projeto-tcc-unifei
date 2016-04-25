from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from tcc import views

admin.autodiscover()

urlpatterns = [
    url(r'^', include('tcc.urls')),
    url(r'^$', 'tcc.views.home', name='home'),
    # url(r'^configuracao/$', 'tcc.views.configuracao', name='configuracao'),
    # url(r'^contato/$', 'tcc.views.contato', name='contato'),
    url(r'^admin/analise/$', views.analise_dados),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^sign_up/', ('tcc.views.register_user'), name='register'),
    url(r'^register_success/', ('tcc.views.register_success')),
    url(r'^confirm/(?P<activation_key>\w+)/', ('tcc.views.register_confirm'), name='register_confirm'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^login/$', 'tcc.views.login_user', name='login'),
]

# urlpatterns += patterns('',
#         url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#             'document_root': settings.STATIC_ROOT,
#         }),
#     )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
