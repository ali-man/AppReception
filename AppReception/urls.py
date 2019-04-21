from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from hsm.ajax import ajax_search_rooms, ajax_info_type_rooms, ajax_booking_post, ajax_search_guest, \
    ajax_status_booking_change, ajax_status_booking_remove
from hsm.views import HomeViews, profile, statistics, TasksViews, GuestsViews, ChessViews, BookingViews, StatusBookingViews, EditBookingViews, DetailBookingViews, user_login, user_logout, user_register

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', HomeViews.as_view(), name='home'),
                  path('login/', user_login, name='login'),
                  path('logout/', user_logout, name='logout'),
                  path('register/', user_register, name='register'),
                  path('chess/', ChessViews.as_view(), name='chess'),
                  path('booking/', BookingViews.as_view(), name='booking'),
                  path('guests/', GuestsViews.as_view(), name='guests'),
                  path('tasks/', TasksViews.as_view(), name='tasks'),
                  path('statistics/', statistics, name='statistics'),
                  path('profile/', profile, name='profile'),
                  path('ajax/status-booking-change/', ajax_status_booking_change, name='ajax-status-booking-change'),
                  path('ajax/status-booking-remove/', ajax_status_booking_remove, name='ajax-status-booking-remove'),
                  path('ajax/search-guest/', ajax_search_guest, name='ajax-search-guest'),
                  path('ajax/booking-post/', ajax_booking_post, name='ajax-booking-post'),
                  path('ajax/search-rooms/', ajax_search_rooms, name='ajax-search-rooms'),
                  path('ajax/info-type-rooms/', ajax_info_type_rooms, name='ajax-info-type-rooms'),
                  path('booking/edit-<int:id>', EditBookingViews.as_view(), name='edit-booking'),
                  path('booking/detail-<int:id>', DetailBookingViews.as_view(), name='detail-booking'),
                  path('booking/status-<int:id>', StatusBookingViews.as_view(), name='status-booking'),
                  # path('api-auth/', include('rest_framework.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
