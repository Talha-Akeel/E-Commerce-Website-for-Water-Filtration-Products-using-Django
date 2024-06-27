from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

# Banner Model
class Banner(models.Model):
    banner_img = models.ImageField(upload_to="banner_images/")
    banner_alt_text = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = '1. Banners'

    def __str__(self):
        return self.banner_alt_text
    
    def image_tag(self):
        return mark_safe("<img src='%s' width='100' />" % (self.banner_img.url))
    
# Product Category model
class ProductCategory(models.Model):
    category_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="product_category_images/")

    def image_tag(self):
        return mark_safe("<img src='%s' width='50' height='50' />" % (self.image.url))

    class Meta:
        verbose_name_plural = '2. Products Categories'

    def __str__(self):
        return self.category_name
    
    # We can also use this, when needed.
    # def __str__(self):
    #     return f"{category_name} ({self.image})"
    

# Product model    
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products_images/")
    slug = models.CharField(max_length=400)
    price=models.PositiveIntegerField(null=True,blank=True,default=0)
    details = models.TextField()
    product_category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '3. Products'

    def __str__(self):
        return self.product_name
    
    def image_tag(self):
        return mark_safe("<img src='%s' width='50' height='50' />" % (self.image.url))
    

# Order
status_choice=(
    ('process','In Process'),
    ('shipped','Shipped'),
    ('delivered','Delivered'),
)
class CartOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total_amount = models.FloatField()
    paid_status = models.BooleanField(default=False)
    order_date_time = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=status_choice,default='process',max_length=150)

    class Meta:
        verbose_name_plural = '4. Orders'

# Order Items
class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    class Meta:
        verbose_name_plural = '5. Order Items'

    def image_tag(self):
        return mark_safe("<img src='/media/%s' width='50' height='50' />" % (self.image))
    

# Address Book
class UserAddressBook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '6. Address'
