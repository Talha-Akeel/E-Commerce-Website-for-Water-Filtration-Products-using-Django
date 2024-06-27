from django.contrib import admin
from .models import Banner,ProductCategory,Product,CartOrder,CartOrderItems, UserAddressBook





class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name','image_tag')
admin.site.register(ProductCategory,ProductCategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_name','image_tag','price','details','product_category','available','is_featured')
    list_editable = ('available','is_featured')
admin.site.register(Product,ProductAdmin)

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ('user','total_amount','paid_status','order_date_time','order_status')
    list_editable = ('paid_status','order_status')
admin.site.register(CartOrder,CartOrderAdmin)

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ('invoice_no','item','image_tag','quantity','price','total')
admin.site.register(CartOrderItems,CartOrderItemsAdmin)

# User Adress Book
class UserAddressBookAdmin(admin.ModelAdmin):
    list_display = ('user','address','status')
    list_editable = ()
admin.site.register(UserAddressBook,UserAddressBookAdmin)

