
from django.urls import path

from api import views

from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns=[

    path('v1/register/',views.SignUpView.as_view()),

    path('v1/token/',ObtainAuthToken.as_view()),

    path("v1/cars/",views.CarListView.as_view()),

    path("v1/car/<int:pk>/",views.CarDetailView.as_view()),

    path("v1/car/<int:pk>/addtofavourites/",views.AddToFavouritesView.as_view()),

    path("v1/favourites/",views.FavouritesListView.as_view()),

    path("v1/favourite/<int:pk>/remove/",views.FavouriteItemDeleteView.as_view()),

    path('v1/order/',views.CheckOutView.as_view()),

    path('v1/orders/summery/',views.Summery.as_view()),

    
]