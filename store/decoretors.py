from django.shortcuts import redirect
from store.models import favouriteitems
from django.contrib import messages



def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"signin required")
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper



def owner_permission_required(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        favour_item=favouriteitems.objects.get(id=id)
        if favour_item.favourites_object.owner != request.user:
            messages.error(request,"permission denied")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
