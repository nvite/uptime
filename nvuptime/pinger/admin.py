from django.contrib import admin
from nvuptime.pinger.models import Group, Endpoint, Ping


class PingAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'disposition', 'response_time', 'created_at', )
    readonly_fields = ('endpoint', 'created_at', 'disposition',
                       'response_time', 'response_code', 'response_headers',
                       'response', )


class PingInline(admin.StackedInline):
    model = Ping
    max_num = 5
    extra = 0
    readonly_fields = ('endpoint', 'created_at', 'disposition',
                       'response_time', 'response_code', 'response_headers',
                       'response', )

admin.site.register(Ping, PingAdmin)


class EndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'url', 'ping_count', 'success_rate',
                    'avg_response_time', 'is_up', 'is_active', )
    list_editable = ('is_active', )
    readonly_fields = ('created_at', 'updated_at', 'is_up', )
    prepopulated_fields = {'slug': ('name', )}
    inlines = [PingInline]

admin.site.register(Endpoint, EndpointAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Group, GroupAdmin)
