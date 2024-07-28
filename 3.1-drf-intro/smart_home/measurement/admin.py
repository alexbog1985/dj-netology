from django.contrib import admin

from measurement.models import Sensor, Measurement


class MeasurementInline(admin.StackedInline):
    model = Measurement
    fields = ['temperature', 'created_at', 'updated_at']
    readonly_fields = fields
    extra = 0


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_filter = ['name', 'description']
    inlines = [MeasurementInline]


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['id', 'temperature', 'created_at', 'updated_at', 'sensor']
    list_display_links = ['id', 'temperature', 'sensor']
    list_filter = ['created_at', 'updated_at', 'sensor']


