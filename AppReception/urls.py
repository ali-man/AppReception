from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from hsm.views import main_page, ChessViews, BookingViews

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', main_page, name='main'),
                  path('chess/', ChessViews.as_view(), name='chess'),
                  path('booking/', BookingViews.as_view(), name='booking'),
                  # path('api-auth/', include('rest_framework.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
