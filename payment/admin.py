from django.contrib import admin
from.models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User

# Register your models here.


admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.site.register(Order)


# order item inline creation 
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
# extend our order model \
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_orderd"]
    fields = ["user" , "full_name","email","shipping_address","amount_paid","date_orderd","shipped","shipped_date"]
    inlines = [OrderItemInline]

# everytime unregister and register the model 
admin.site.unregister(Order)

# regeister Order 
admin.site.register(Order, OrderAdmin)
