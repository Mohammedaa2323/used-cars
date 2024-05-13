from rest_framework import serializers

from django.contrib.auth.models import User

from store.models import  Brand,Fuel,Cars,favouriteitems,favourites,Booking


class UserSerializer(serializers.ModelSerializer):
     
    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
   
    class Meta:
        model=User

        fields=["id","username","email","password1","password2","password"]

        read_only_fields=["id","password"]

    def create(self, validated_data):
         
         password1=validated_data.pop("password1")

         password2=validated_data.pop("password2")

         if password1!=password2:
              
              raise serializers.ValidationError("password missmatch")
         else:
              
              return User.objects.create_user(**validated_data,password=password1)


class BrandSerializers(serializers.ModelSerializer):

    class Meta:

        model=Brand

        fields=["id","name"]

class FuelSerializers(serializers.ModelSerializer):

    class Meta:

        model=Fuel

        fields=["id","fuel"]


class CarSerializers(serializers.ModelSerializer):

        brand_object=BrandSerializers(read_only=True)

        fuel_object=FuelSerializers(read_only=True)

        class Meta:
             
             model=Cars

             fields="__all__"


class CartcarsSerializers(serializers.ModelSerializer):
     
     class Meta:
          
        model=Cars
        fields=["id","name","price","image","year","Registration"]


class FavouritesItemSerializers(serializers.ModelSerializer):
     
    cars_object=CartcarsSerializers(read_only=True)
    

    class Meta:
         
         model=favouriteitems

         fields=[
              "id",
              "cars_object",
              "created_date"
         ]

class FavouritesSerializers(serializers.ModelSerializer):
     
     cart_items=FavouritesItemSerializers(many=True)

     owner=serializers.StringRelatedField()

     # cars_object=CartcarsSerializers(read_only=True)


     class Meta:
          
          model=favourites

          fields=[
               "id",
               "owner",
               "cart_items"
          ]


class OrderSerializer(serializers.ModelSerializer):


     favourite_item_object=FavouritesItemSerializers(many=True,read_only=True)

     order_object=serializers.StringRelatedField()

     class Meta:

          model=Booking

          fields="__all__"