from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

# mix profile info and user info 
class ProfileInline(admin.StackedInline):
    model = Profile

# extend User model 

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username","first_name","last_name","email"]
    inlines = [ProfileInline]

# unregister the old way
admin.site.unregister(User)


# register the new way 

admin.site.register(User, UserAdmin)



