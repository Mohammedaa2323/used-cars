from django.shortcuts import render

# Create your views here.

from store.models import Cars,Brand,Fuel,favouriteitems,favourites,Booking,BookingItems

from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView

from django.contrib.auth.models import User

from api.serializers import FuelSerializers,BrandSerializers,CarSerializers,UserSerializer,CartcarsSerializers,FavouritesSerializers,FavouritesItemSerializers,OrderSerializer

from rest_framework import status

from rest_framework import authentication,permissions

import razorpay




class SignUpView(CreateAPIView):

    serializer_class=UserSerializer

    queryset=User.objects.all()


class CarListView(ListAPIView):

    serializer_class=CarSerializers 

    queryset=Cars.objects.all()

    
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]



class CarDetailView(RetrieveAPIView):

    serializer_class=CarSerializers

    queryset=Cars.objects.all()

    
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


class AddToFavouritesView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def post(self,request,*args,**kwargs):

        favourites_object=request.user.cart

        id=kwargs.get("pk")

        cars_object=Cars.objects.get(id=id)


        favouriteitems.objects.create(

            favourites_object=favourites_object,
            cars_object=cars_object,

        )

        return Response(data={"message":"selected"})
    

class FavouritesListView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        qs=request.user.cart

        serializer_instance=FavouritesSerializers(qs)

        return Response(data=serializer_instance.data)
    

class FavouriteItemDeleteView(DestroyAPIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    serializer_class=FavouritesItemSerializers

    queryset=favouriteitems.objects.all()


class CheckOutView(APIView):


    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def post(self,request,*args,**kwargs):

        user_obj=request.user

        phone=request.data.get("phone")

        email=request.data.get("email")

        payment=request.data.get("payment")

        order_obj=Booking.objects.create(


            user_object = user_obj,
            email=email,
            phone=phone,
            payment=payment
          )



        cart_items=request.user.cart.cart_items

        for bi in cart_items:

            booking_instance= BookingItems.objects.create(
                        order_object=order_obj,
                        favourite_item_object=bi

            )
            
            bi.is_paid=True

            bi.save()

        if payment == "online" and booking_instance:


            client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


            data = { "amount": 2000*100, "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)

            print(payment)

            order_id = payment.get("id")

            key_id=KEY_ID

            user=request.user.username

            data={
                "order_id":order_id,
                "key_id":key_id,
                "user":user,
                "phone":phone
            }

            booking_instance.order_id = order_id

            booking_instance.save()

            return Response(data=data,status=status.HTTP_201_CREATED)




class Summery(ListAPIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    serializer_class=OrderSerializer

    queryset=Booking.objects.all()


    def get_queryset(self):
        return Booking.objects.filter(user_object=self.request.user)
    
