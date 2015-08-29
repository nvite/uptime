from django.contrib import admin
from nvuptime.pinger.models import Group, Endpoint, Ping


class PingAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'disposition', 'response_time', 'created_at', )
    list_filter = ('endpoint__group', 'disposition')
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
    list_display = ('title', 'slug', 'url', 'group', 'ping_count', 'success_rate',
                    'avg_response_time', 'is_up', 'is_active', )
    list_editable = ('is_active', )
    list_filter = ('is_up', 'is_active', 'group', )
    readonly_fields = ('created_at', 'updated_at', 'is_up', )
    prepopulated_fields = {'slug': ('title', )}
    # inlines = [PingInline]

admin.site.register(Endpoint, EndpointAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', )
    prepopulated_fields = {'slug': ('title', )}

admin.site.register(Group, GroupAdmin)
