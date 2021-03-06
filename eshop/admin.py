from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Gallery)
admin.site.register(Return)
admin.site.register(FooterContactInfo)
admin.site.register(HomepageBanner)

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)

class SubCategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)



