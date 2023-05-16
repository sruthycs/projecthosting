from django.contrib import admin
from dairyapp.models import Products,Services,categories,Billing,Profile,user_address,ReviewRating
# Register your models here.

search_fields = 'prd name'
admin.site.register (Products)
admin.site.register (Services)
admin.site.register (categories)
admin.site.register (Billing)
admin.site.register (Profile)
admin.site.register (user_address)
admin.site.register (ReviewRating)
# @admin.register(Cart)
# class CartModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'product', 'quantity']
