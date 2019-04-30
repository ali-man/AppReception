from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from hsm.ajax import ajax_search_booking_id, ajax_send_booking_group, ajax_evict_send, ajax_guest_add, ajax_booking_info, ajax_new_chess, ajax_search_rooms, ajax_info_type_rooms, ajax_booking_post, ajax_search_guest, \
    ajax_status_booking_change, ajax_status_booking_remove

app_name = 'ajax'
urlpatterns = [
    path('evict-send/', ajax_evict_send, name='ajax-evict-send'),
    path('booking-info/', ajax_booking_info, name='ajax-booking-info'),
    path('send-booking-group/', ajax_send_booking_group, name='ajax-send-booking-group'),
    path('search-booking-id/', ajax_search_booking_id, name='ajax-search-booking-id'),
    path('new-chess/', ajax_new_chess, name='ajax-new-chess'),
    path('status-booking-change/', ajax_status_booking_change, name='ajax-status-booking-change'),
    path('status-booking-remove/', ajax_status_booking_remove, name='ajax-status-booking-remove'),
    path('search-guest/', ajax_search_guest, name='ajax-search-guest'),
    path('booking-post/', ajax_booking_post, name='ajax-booking-post'),
    path('guest-add/', ajax_guest_add, name='ajax-guest-add'),
    path('search-rooms/', ajax_search_rooms, name='ajax-search-rooms'),
    path('info-type-rooms/', ajax_info_type_rooms, name='ajax-info-type-rooms'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
