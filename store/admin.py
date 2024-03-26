from django.contrib import admin
from store.models import Brand,Cars,Fuel,Booking,favouriteitems

# Register your models here.


admin.site.register(Brand)
admin.site.register(Cars)
admin.site.register(Fuel)
admin.site.register(Booking)
admin.site.register(favouriteitems)