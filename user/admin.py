from django.contrib import admin
from .models import FoodGrain, Location,AppUser,Farms,Warehouse, Centre, Demand
# Register your models here.
class FoodGrainAdmin(admin.ModelAdmin):
    list_display = ('type', 'life')
admin.site.register(FoodGrain,FoodGrainAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('xloc', 'yloc')
admin.site.register(Location,LocationAdmin)

class AppUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'address', 'dob')
admin.site.register(AppUser,AppUserAdmin)


admin.site.register(Farms)

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('sect', 'free', 'total')
admin.site.register(Warehouse,WarehouseAdmin)

admin.site.register(Centre)
admin.site.register(Demand)