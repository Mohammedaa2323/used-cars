from django.shortcuts import render,redirect
from django.views import View
from store.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator 
from django.views.decorators.cache import never_cache
from store.decoretors import signin_required,owner_permission_required
import razorpay
from django.views.decorators.csrf import csrf_exempt


from store.models import Cars,Brand,favouriteitems,Booking,BookingItems
# Create your views here.




class SignupView(View):
    

    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        return render(request,"login.html",{"form":form})



class SigninView(View):


    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
         u_name=form.cleaned_data.get("username")
         pwd=form.cleaned_data.get("password")
         user_object=authenticate(request,username=u_name,password=pwd)
         if user_object:
             login(request,user_object)
             return redirect("index")
         messages.error(request,"invalid credontion")
        return render(request,"login.html",{"form":form})

@method_decorator([signin_required,never_cache],name="dispatch")
class SignoutView(View):


    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

@method_decorator([signin_required,never_cache],name="dispatch")
class IndexView(View):
    

    def get(self,request,*args,**kwargs):
        qs=Cars.objects.all()
        brand=Brand.objects.all()
        selected_brands=request.GET.get("brands")
        if selected_brands:
            qs=qs.filter(brand_object__name=selected_brands)
        return render(request,"index.html",{"data":qs,"brands":brand})

    
    def post(self,request,*args,**kwargs):


        brand_name=request.POST.get("brand")
        qs=Cars.objects.filter(brand_object__name=brand_name)
        return render(request,"index.html",{"data":qs})


@method_decorator([signin_required,never_cache],name="dispatch")
class CarsDetailView(View):
    

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Cars.objects.get(id=id)
        return render(request,"cars_detail.html",{"data":qs})
    


@method_decorator([signin_required,never_cache],name="dispatch")
class AddToFavouritesView(View):


    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        cars_obj=Cars.objects.get(id=id)
        favouriteitems.objects.create(
            cars_object=cars_obj,
            favourites_object=request.user.cart
        )
        return redirect("index")
    
@method_decorator([signin_required,never_cache],name="dispatch")
class FavouriteslistView(View):


    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitem.all()
        return render(request,"favourites_list.html",{"data":qs})


@method_decorator([signin_required,owner_permission_required],name="dispatch")
class FavouroiteRemoveView(View):


    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        favouriteitems.objects.get(id=id).delete()
        return redirect("favourites-list")
    

class CheckOutView(View):


    def get(self,request,*args,**kwargs):
        return render(request,"checkout.html")
    

    def post(self,request,*args,**kwargs):
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        payment_method=request.POST.get("payment")

    # creat order_instance
        order_obj=Booking.objects.create(


            user_object=request.user,
            email=email,
            phone=phone,
            payment=payment_method
          )

             # creat order_item_instance

        try:  #if there any error in this method we can use try
            basket_items=request.user.cart.cart_items
            for bi in basket_items:

                BookingItems.objects.create(
                    order_object=order_obj,
                    favourite_item_object=bi

                )
                bi.is_order_placed=True
                bi.save()
        

        except: # if the method was wrong we also send the solution for the method

            return redirect("index")

        finally:  # if this method sucsses or wrong this method work allways
           
           if payment_method=="online" and order_obj:
                            
                client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

                data = { "amount": 2000*100, "currency": "INR", "receipt": "order_rcptid_11" }
                payment = client.order.create(data=data)

                order_obj.order_id=payment.get("id")
                order_obj.save()

                print("payment initiate",payment)
                context={
                    "key":KEY_ID,
                    "order_id":payment.get("id"),
                    "amount":payment.get("amount")
                }
                return render(request,"payment.html",{"context":context})
           return redirect("index")



class OrderSummery(View):


    def get(self,requset,*args,**kwargs):
        # is_order=requset.user.purchase.all()
        is_order=Booking.objects.filter(user_object=requset.user).exclude(status="cancelled")
        print("AUTH USER====",requset.user,"============")
        return render(requset,"order_summery.html",{"data":is_order})
    
class BookinggItemsRemove(View):


    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        BookingItems.objects.get(id=id).delete()
        return redirect('order-summery')
    

@method_decorator(csrf_exempt,name="dispatch")

class PaymentVarificationView(View):

    def post(self,request,*args,**kwargs):
        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))
        data=request.POST
        print(request.POST,"hello")

        try:
            client.utility.verify_payment_signature(data)
            order_obj=Booking.objects.get(order_id=data.get("razorpay_order_id"))
            order_obj.is_paid=True
            order_obj.save()
            print("************ Transaction complete********")
        except:
            print("!!!!!!!!!!!!!transaction falid!!!!!!!!!")

        return redirect("order-summery")



