from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from hsm.chess import ChessViews
from hsm.views import EditServicesViews, \
    checks_list, \
    print_booking, \
    organization, \
    add_guest, \
    HomeViews, \
    profile, \
    statistics, \
    TasksViews, \
    GuestsViews, \
    BookingViews, \
    StatusBookingViews, \
    EditBookingViews, \
    DetailBookingViews, \
    user_login, \
    user_logout, \
    user_register, \
    ListBookingViews, \
    printer, \
    ListServicesViews, \
    CreateServicesViews
from hsm.new_chess import NewChessViews

admin.site.site_header = 'Панель управления'
urlpatterns = [
                  path('', HomeViews.as_view(), name='home'),
                  path('chess/', ChessViews.as_view(), name='chess'),
                  path('print/<str:_date>', printer, name='print'),
                  path('admin/', admin.site.urls),
                  path('checks/', checks_list, name='checks-list'),
                  path('login/', user_login, name='login'),
                  path('logout/', user_logout, name='logout'),
                  path('register/', user_register, name='register'),
                  path('booking/', BookingViews.as_view(), name='booking'),
                  path('booking/print-<int:id>', print_booking, name='booking-print'),
                  path('guests/', GuestsViews.as_view(), name='guests'),
                  path('guests/add/', add_guest, name='guest-add'),
                  path('bookings/', ListBookingViews.as_view(), name='list-booking'),
                  path('organization/', organization, name='organization'),
                  path('tasks/', TasksViews.as_view(), name='tasks'),
                  path('statistics/', statistics, name='statistics'),
                  path('services/list', ListServicesViews.as_view(), name='services-list'),
                  path('services/edit-<int:pk>', EditServicesViews.as_view(), name='services-edit'),
                  path('services/create', CreateServicesViews.as_view(), name='services-create'),
                  path('profile/', profile, name='profile'),
                  path('new-chess/', NewChessViews.as_view(), name='new-chess'),
                  path('ajax/', include('hsm.urls'), name='ajax'),
                  path('booking/edit-<int:id>', EditBookingViews.as_view(), name='edit-booking'),
                  path('booking/detail-<int:id>', DetailBookingViews.as_view(), name='detail-booking'),
                  path('booking/status-<int:id>', StatusBookingViews.as_view(), name='status-booking'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
