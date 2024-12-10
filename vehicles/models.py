from django.db import models
from datetime import timedelta
from .utils import adjust_end_time

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
        ('decommissioned', 'Decommissioned'),
    ]

    VEHICLE_TYPE_CHOICES = [
        ('4W', '4W [Upto 5mt] [10-14ft bed]'),
        ('6W', '6W [9-12mt] [18ft bed]'),
        ('14W', '14W [30mt] [24-28ft bed]'),
        ('16W_35mt', '16W [35mt] [24-32ft bed]'),
        ('22W', '22W [42-45mt] [40ft Trailor bed]'),
        ('18W', '18W [40mt] [40ft Trailor bed]'),
        ('10W', '10W [16-21mt] [20-22ft bed]'),
        ('16W_32mt', '16W [32mt] [40ft Trailor bed]'),
        ('12W', '12W [25mt] [22-24ft bed]'),
        ('Others', 'Others'),
    ]
    vehicle_number = models.CharField(max_length=20, primary_key=True)
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPE_CHOICES)
    avg_speed_per_hour = models.IntegerField()
    cost = models.FloatField()
    commission_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
    	return f"{self.vehicle_number} - {self.vehicle_type}"



class Driver(models.Model):
    DRIVER_STATUS = [
        ('active','Active'),
        ('inactive','Inactive'),
    ]
    driver_id = models.CharField(max_length=12, primary_key=True, editable=False)
    driver_contact = models.IntegerField(unique=True)
    driver_name = models.CharField(max_length=100)
    salary_pm = models.FloatField()
    driver_status = models.CharField(max_length =30, choices=DRIVER_STATUS)

    def save(self, *args, **kwargs):
        if not self.driver_id:
            # Generate `driver_id` with prefix `DR` and an incremented number
            last_driver = Driver.objects.all().order_by('driver_id').last()
            if last_driver:
                last_id = int(last_driver.driver_id.replace('DR', ''))
                self.driver_id = f"DR{last_id + 1:06d}"  # Zero-padded to 4 digits
            else:
                self.driver_id = "DR000001"  # Start from DR0001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.driver_name} ({self.driver_id})"

class Trip(models.Model):
    trip_id = models.CharField(max_length=12, primary_key=True, editable=False)
    start_point = models.CharField(max_length=100)  # Could also use a geolocation field
    end_point = models.CharField(max_length=100, blank=True, null=True)  # Computed
    load = models.FloatField()  # In MT
    margin = models.FloatField(help_text="Percentage between 0-100")  # Percentage
    trip_time = models.DurationField(blank=True, null=True)  # Computed
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)  # Computed
    trip_distance = models.FloatField(default='0')  # Computed (in KM)
    driver_cost = models.FloatField(blank=True, null=True)  # Computed
    driver_allowance = models.FloatField() #input from user
    no_restriction_timezone = models.BooleanField(default=False)

    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, default='DR000001', limit_choices_to={'driver_status': 'active'}, related_name='trips')
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, default='KA02M1221', limit_choices_to={'status': 'active'}, related_name='trips')
    
    def save(self, *args, **kwargs):
        # Generate unique Trip ID
        if not self.trip_id:
            last_trip = Trip.objects.all().order_by('trip_id').last()
            if last_trip:
                last_id = int(last_trip.trip_id.replace('TR', ''))
                self.trip_id = f"TR{last_id + 1:06d}"
            else:
                self.trip_id = "TR000001"
        
        # Compute end time based on trip distance, average speed, and restrictions
        if self.trip_distance and self.start_time:
            avg_speed_kmph = Vehicle.objects.get().avg_speed_per_hour  # Fetch vehicle data
            trip_duration_hours = self.trip_distance / avg_speed_kmph
            computed_end_time = self.start_time + timedelta(hours=trip_duration_hours)
            
            if self.no_restriction_timezone:
                computed_end_time = adjust_end_time(computed_end_time)
            
            self.end_time = computed_end_time
            self.trip_time = computed_end_time - self.start_time
        
        # Compute driver cost
        if self.trip_time:
            driver = Driver.objects.get()  # Fetch appropriate driver details
            monthly_hours = 30 * 24
            driver_hourly_rate = driver.salary_pm / monthly_hours
            self.driver_cost = driver_hourly_rate * self.trip_time.total_seconds() / 3600
        
        super().save(*args, **kwargs)

class AdhocCost(models.Model):
    COST_TYPES = [
        ('fuel', 'Fuel'),
        ('maintenance', 'Maintenance'),
        ('toll', 'Toll'),
        ('misc', 'Miscellaneous'),
    ]
    adhoc_cost_id = models.CharField(max_length=12, primary_key=True, editable=False)
    trip = models.ForeignKey(Trip, related_name='adhoc_costs', on_delete=models.CASCADE)
    cost = models.FloatField()
    cost_type = models.CharField(max_length=20, choices=COST_TYPES)

    def save(self, *args, **kwargs):
        if not self.adhoc_cost_id:
            last_cost = AdhocCost.objects.all().order_by('adhoc_cost_id').last()
            if last_cost:
                last_id = int(last_cost.adhoc_cost_id.replace('AC', ''))
                self.adhoc_cost_id = f"AC{last_id + 1:06d}"
            else:
                self.adhoc_cost_id = "AC000001"
        super().save(*args, **kwargs)
