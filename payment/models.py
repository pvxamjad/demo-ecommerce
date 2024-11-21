from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save,pre_save
import datetime
from django.dispatch import receiver




class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_first_name = models.CharField(max_length=255)
    shipping_last_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255,null=True,blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255)
    shipping_pincode = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=255)

    # dont pluralize address 
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f"shipping address - {str(self.id)}"
    
# create a user shipping by default when user sign in 
def create_shipping(sender, instance, created ,**kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

# automate the profile thing 
post_save.connect(create_shipping, sender=User)
    

class Order(models.Model):
    #foreign key
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=10000)
    amount_paid = models.DecimalField(max_digits=7,decimal_places=2)
    date_orderd = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    shipped_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return f"Order - {str(self.id)}"
    
# auto add shiiping date 
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender,instance, **kwargs):
    if instance.pk :
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.shipped_date = now


class OrderItem(models.Model):
    # foriegn keys 
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"Order Item {str(self.id)}"

    