from django.conf.urls import include, url
from django.contrib import admin
import settings  
urlpatterns = [
    # Examples:
    # url(r'^$', 'd_login.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^xadmin/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', include('login.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_ROOT }),
]
