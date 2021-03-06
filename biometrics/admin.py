from django.contrib import admin

from biometrics.models import Client, Entry


class InlineEntryAdmin(admin.TabularInline):
    model = Entry
    ordering = ['-date']
    extra = 0


class ClientAdmin(admin.ModelAdmin):
    readonly_fields = ('metrics_link',)
    inlines = [InlineEntryAdmin]


admin.site.register(Client, ClientAdmin)
admin.site.register(Entry)
