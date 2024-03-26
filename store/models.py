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

    @property
    def cart_items(self):
        return self.cartitem.filter(is_order_placed=False)

class favouriteitems(models.Model):
    cars_object=models.ForeignKey(Cars,on_delete=models.CASCADE)
    favourites_object=models.ForeignKey(favourites,on_delete=models.CASCADE,related_name="cartitem")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_order_placed=models.BooleanField(default=False)



    

def create_cart(sender,instance,created,**kwargs):
    # created=T|F
    # sender=User
    # instance=the user
    if created:
        favourites.objects.create(owner=instance)
post_save.connect(create_cart,sender=User)


class Booking(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    phone=models.CharField(max_length=12)
    email=models.EmailField(max_length=200,null=True)
    is_paid=models.BooleanField(default=False)
    order_id=models.CharField(max_length=200,null=True)
    payment=models.CharField(max_length=200,default="online")

    option=(
        ("order-booked","order-booked"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=option,default="order-booked")


    @property
    def get_order_items(self):
        return self.purchaseitems.all()
    
    # @property
    # def get_order_total(self):
    #     purchase_items=self.get_order_items
    #     order_total=0
    #     if purchase_items:
    #         order_total=sum([pi.basket_item_object.item_total for pi in purchase_items])
    #     return order_total
     
class BookingItems(models.Model):
    order_object =models.ForeignKey(Booking,on_delete=models.CASCADE,related_name="purchaseitems")
    favourite_item_object=models.ForeignKey(favouriteitems,on_delete=models.CASCADE)
    


