from django.contrib import admin


# import models
from orders.models import *

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Item)
admin.site.register(Style)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Size)
admin.site.register(SubKind)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner_Platter)