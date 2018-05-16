from django.contrib import admin

from .models import Client, Contractor, Business, BusinessType, Event, Opinion


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    class EventInline(admin.TabularInline):
        model = Event
        extra = 1
        show_change_link = True
        fields = ('title', 'businesses', 'date_from', 'date_to')

    inlines = [EventInline]
    list_display = ('user',)
    list_filter = ('user__date_joined',)
    search_fields = ('user',)


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):

    class BusinessInline(admin.StackedInline):
        model = Business
        extra = 1
        show_change_link = True

    inlines = [BusinessInline]
    list_display = ('user',)
    list_filter = ('user__date_joined',)
    search_fields = ('user',)


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):

    class OpinionInline(admin.StackedInline):
        model = Opinion
        extra = 1
        show_change_link = True
        fields = ('text', 'rating')

    inlines = [OpinionInline]
    fields = ('name', 'owner', 'business_type')
    list_display = ('name', 'owner', 'business_type', 'get_average_rating')
    list_filter = ('business_type',)
    search_fields = ('name',)


@admin.register(BusinessType)
class BusinessTypeAdmin(admin.ModelAdmin):
    search_fields = ('business_type',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'owner', 'businesses')
        }),
        ('Date information', {
            'fields': ('date_from', 'date_to'),
            'classes': ('collapse',)
        })
    )
    list_display = ('title', 'date_from', 'date_to', 'get_duration', 'owner')
    list_filter = ('date_from', 'date_to')
    search_fields = ('title',)


@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    fields = ('text', 'rating', 'business')
    list_display = ('__str__', 'rating', 'business')
    list_filter = ('rating',)
