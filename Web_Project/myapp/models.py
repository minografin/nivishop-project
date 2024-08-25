from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFileName(request, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s" % (now_time, filename)
    return os.path.join('uploads/', filename)

# Create your models here.
class category(models.Model):
    Name = models.CharField(max_length=250, null=False, blank=False)
    image = models.ImageField(upload_to=getFileName, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show, 1-hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Name

class Product(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE, default=True)
    Name = models.CharField(max_length=150, null=False, blank=False)
    vendor = models.CharField(max_length=150, null=False, blank=False)
    Product_image = models.ImageField(upload_to=getFileName, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(max_length=150, null=False, blank=False)
    sales_price = models.FloatField(max_length=150, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show, 1-hidden")
    trending = models.BooleanField(default=False, help_text="0-default, 1-trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Name

class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    @property
    def total_cast(self):
        return self.product_qty*self.product.sales_price