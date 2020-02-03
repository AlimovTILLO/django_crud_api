from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from .settings import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url('admin/', admin.site.urls),
    url('api/', include('api.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
