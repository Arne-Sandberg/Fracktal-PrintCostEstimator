from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
url(r'^home/$', views.contact),
url(r'^login/$', login, {'template_name':'login_app/login.html'}),
url(r'^logout/$', logout, {'template_name':'login_app/logout.html'}),
url(r'^register/$', views.register, name="register"),
url(r'^contact/$', views.contact, name="contact"),
url(r'^contact_success/$', views.contact_success, name="contact_success"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
