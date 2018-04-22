from django.contrib import admin
from .models import Client, Contractor, Business, BusinessType, Event


class EventInline(admin.TabularInline):
    model = Event
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [
        EventInline,
    ]
    list_display = ['user']


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    pass


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessType)
class BusinessTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
