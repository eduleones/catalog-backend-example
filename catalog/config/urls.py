from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf.swagger_utils import get_swagger_view

docs_view = get_swagger_view(title='Catalog')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', docs_view),
    path(
        'shoes/',
        include(('shoes.urls', 'shoes'), namespace='shoes')
    ),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
