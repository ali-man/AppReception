from django.contrib import admin

from hsm.models import Rooms, TypeRoom


class RoomsLine(admin.TabularInline):
    model = Rooms
    extra = 0


class TypeRoomAdmin(admin.ModelAdmin):
    fields = ('name', 'price')
    inlines = [RoomsLine]


admin.site.register(TypeRoom, TypeRoomAdmin)
