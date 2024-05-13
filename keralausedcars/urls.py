"""
URL configuration for keralausedcars project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from store import views
from django.conf import settings
from django.conf.urls.static import static

# from api import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignupView.as_view(),name="login"),
    path('signin/',views.SigninView.as_view(),name="signin"),
    path('singout/',views.SignoutView.as_view(),name="signout"),
    path('index/',views.IndexView.as_view(),name="index"),
    path('cars/<int:pk>/details/',views.CarsDetailView.as_view(),name="cars-details"),
    path('cars/<int:pk>/add_to_favourites/',views.AddToFavouritesView.as_view(),name="addto-favourites"),
    path('car/favourites/list/',views.FavouriteslistView.as_view(),name="favourites-list"),
    path('car/<int:pk>/remove/',views.FavouroiteRemoveView.as_view(),name="favourites-remove"),
    path('chackout/',views.CheckOutView.as_view(),name="checkout"),
    path('summery/',views.OrderSummery.as_view(),name="order-summery"),
    path('order/item/<int:pk>/remove/',views.BookinggItemsRemove.as_view(),name="order-item-remove"),

    path('payment/verification/',views.PaymentVarificationView.as_view(),name="payment-varification"),

    path("api/",include("api.urls"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

