from django.contrib import admin

from hsm.models import Rooms, TypeRoom, Booking, Citeznship, PaymentServices, Services


class RoomsLine(admin.TabularInline):
    model = Rooms
    extra = 1


class PaymentServicesLine(admin.TabularInline):
    model = PaymentServices
    extra = 1


class TypeRoomAdmin(admin.ModelAdmin):
    # fields = ('name', 'price_uzs', 'price_usd')
    list_display = ['name', 'price_uzs', 'price_usd']
    list_display_links = ['name']
    inlines = [RoomsLine]


admin.site.register(TypeRoom, TypeRoomAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'date_arrival', 'date_departure']
    list_display_links = ['id']


admin.site.register(Booking, BookingAdmin)


class CiteznshipAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id']


admin.site.register(Citeznship, CiteznshipAdmin)


class ServicesAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'paid']
    list_display_links = ['id']
    inlines = [PaymentServicesLine]


admin.site.register(Services, ServicesAdmin)
