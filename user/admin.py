from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import FoodGrain, Location,User,Farms,Warehouse, Centre, Demand
from .forms import CustomUserChangeForm, CustomUserCreationForm
# Register your models here.
class FoodGrainAdmin(admin.ModelAdmin):
    list_display = ('id','type', 'life')
admin.site.register(FoodGrain,FoodGrainAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('xloc', 'yloc')
admin.site.register(Location,LocationAdmin)

# class AppUserAdmin(UserAdmin):
#     list_display = ('name', 'contact', 'address', 'dob')


"""name=models.CharField(max_length=300)
    contact=models.CharField(max_length=12)
    address=models.TextField()
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    dob=models.DateField(null = True)
    adhaar
"""

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    UserAdmin.add_fieldsets += (
        (None, {
            'classes': ('wide',),
            'fields': ('name','contact', 'address', 'city','state', 'dob','adhaar','role')}
        ),
    )
    UserAdmin.fieldsets += (
        (None, {
            'classes': ('wide',),
            'fields': ('name','contact', 'address', 'city','state', 'dob','adhaar','role')}
        ),
    )
    # list_display = ['email','contact','user_type','otp', 'bquiz_score', 'verified']

admin.site.register(User, CustomUserAdmin)






admin.site.register(Farms)

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('sector', 'free_space', 'total_space')
admin.site.register(Warehouse,WarehouseAdmin)

admin.site.register(Centre)
admin.site.register(Demand)


# # Register your models here.
# admin.site.register(User)
