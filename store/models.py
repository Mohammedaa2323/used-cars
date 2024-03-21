from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


class Brand(models.Model):
    name=models.CharField(max_length=250,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
# class CarModel(models.Model):
#     car_model=models.CharField(max_length=250)
#     created_date=models.DateTimeField(auto_now_add=True)
#     updated_date=models.DateTimeField(auto_now=True)
#     is_active=models.BooleanField(default=True)

#     def __str__(self):
#         return self.car_model
    
class Fuel(models.Model):
    fuel=models.CharField(max_length=200)

    def __str__(self):
        return self.fuel


class Cars(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(null=True)
    brand_object=models.ForeignKey(Brand,on_delete=models.DO_NOTHING,related_name="item")
    year=models.PositiveIntegerField()
    Registration=models.CharField(max_length=200)
    image=models.ImageField(upload_to="car_images",default="default.jpg",null=True,blank=True)
    fuel_object=models.ForeignKey(Fuel,on_delete=models.DO_NOTHING,default=0)
    distance_travelled=models.PositiveIntegerField()
    price=models.PositiveIntegerField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_sold=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    

class favourites(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)


class favouriteitems(models.Model):
    cars_object=models.ForeignKey(Cars,on_delete=models.CASCADE)
    favourites_object=models.ForeignKey(favourites,on_delete=models.CASCADE,related_name="cartitem")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

def create_cart(sender,instance,created,**kwargs):
    # created=T|F
    # sender=User
    # instance=the user
    if created:
        favourites.objects.create(owner=instance)
post_save.connect(create_cart,sender=User)