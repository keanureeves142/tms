from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import VehicleForm, DriverForm, TripForm, AdhocCostForm
from .models import Vehicle, Driver, Trip, AdhocCost
from django.conf import settings

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    paginator = Paginator(vehicles, 10)  # Show 10 vehicles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'vehicles/vehicle_list.html', {'page_obj': page_obj})

def vehicle_add(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'vehicles/vehicle_form.html', {'form': form})

def vehicle_update(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicles/vehicle_form.html', {'form': form})


def landing(request):
    return render(request,'vehicles/landing.html')



def driver_list(request):
    driver = Driver.objects.all()
    paginator = Paginator(driver, 10)  # Show 10 vehicles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'driver/driver_list.html', {'page_obj': page_obj})

def driver_add(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm()
    return render(request, 'driver/driver_form.html', {'form': form})

def driver_update(request, pk):
    if pk:  # Edit existing driver
        driver = get_object_or_404(Driver, pk=pk)
    else:  # Add new driver
        driver = None
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm(instance=driver)
    return render(request, 'driver/driver_form.html', {'form': form})


def trip_create(request):
    drivers = Driver.objects.filter(driver_status='active')  # Query only active drivers
    vehicles = Vehicle.objects.filter(status='active')  # Query only active vehicles

    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trip_list')
    else:
        form = TripForm()
    return render(request, 'trip/trip_form.html', {'form': form, 'drivers': drivers, 'vehicles': vehicles})

def adhoc_cost_create(request, trip_id):
    trip = Trip.objects.get(trip_id=trip_id)
    if request.method == 'POST':
        form = AdhocCostForm(request.POST)
        if form.is_valid():
            adhoc_cost = form.save(commit=False)
            adhoc_cost.trip = trip
            adhoc_cost.save()
            return redirect('trip_detail', trip_id=trip_id)
    else:
        form = AdhocCostForm()

    return render(request, 'adhoc_cost/adhoc_cost_form.html', {'form': form, 'trip': trip})


def get_driver_details(request, driver_id):
    try:
        driver = Driver.objects.get(driver_id=driver_id)
        data = {
            'salary_pm': driver.salary_pm,
        }
        return JsonResponse(data)
    except Driver.DoesNotExist:
        return JsonResponse({'error': 'Driver not found'}, status=404)

def get_vehicle_details(request, vehicle_number):
    try:
        vehicle = Vehicle.objects.get(vehicle_number=vehicle_number)
        data = {
            'cost': vehicle.cost,  # Assuming you have an `age` field or can compute it
            'avg_speed_per_hour': vehicle.avg_speed_per_hour,
            'commission_date' :vehicle.commission_date,
        }
        return JsonResponse(data)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)