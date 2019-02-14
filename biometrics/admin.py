from django.contrib import admin

from biometrics.models import Client, Entry


class ClientAdmin(admin.ModelAdmin):
    readonly_fields = ('metrics_link',)


admin.site.register(Client, ClientAdmin)
admin.site.register(Entry)
