from django.contrib import admin

from hsm.models import Rooms, TypeRoom, Booking


class RoomsLine(admin.TabularInline):
    model = Rooms
    extra = 0


class TypeRoomAdmin(admin.ModelAdmin):
    fields = ('name', 'price_uzs', 'price_usd')
    inlines = [RoomsLine]


admin.site.register(TypeRoom, TypeRoomAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'date_arrival', 'date_departure']
    list_display_links = ['id']

admin.site.register(Booking, BookingAdmin)
