from django.shortcuts import render,redirect
from django.views import View
from store.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from store.models import Cars,Brand,favouriteitems
# Create your views here.


class SignupView(View):
    

    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request,"login.html",{"form":form})

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

class SigninView(View):


    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
    
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
        return render(request,"signin.html",{"form":form})




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

class CarsDetailView(View):
    

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Cars.objects.get(id=id)
        return render(request,"cars_detail.html",{"data":qs})
    

class AddToFavouritesView(View):


    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        cars_obj=Cars.objects.get(id=id)
        favouriteitems.objects.create(
            cars_object=cars_obj,
            favourites_object=request.user.cart
        )
        return redirect("index")