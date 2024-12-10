from django.contrib import admin
from .models import Vehicle, Driver, Trip, AdhocCost

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'vehicle_type', 'avg_speed_per_hour', 'cost', 'commission_date', 'status')
    list_filter = ('status',)
    search_fields = ('vehicle_number', 'vehicle_type')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('driver_id', 'driver_name', 'salary_pm', 'driver_status')
    list_filter = ('driver_status',)
    search_fields = ('driver_name', 'driver_id')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('trip_id','start_point','end_point','load','margin','trip_time',
        'start_time','end_time','trip_distance','driver_cost','driver_allowance','no_restriction_timezone')

@admin.register(AdhocCost)
class AdhocCostAdmin(admin.ModelAdmin):
    list_display = ('adhoc_cost_id', 'trip', 'cost', 'cost_type')