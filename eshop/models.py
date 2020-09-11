from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.validators import validate_email
import uuid

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True, unique=True, validators=[validate_email])
    stripe_id = models.CharField(max_length=200, null=True, default='')

    def __str__(self):
        return str(self.user)

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(default='   ')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    description = models.TextField(max_length=500, default="")
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    STATUS = (
        ('Ordering', 'Ordering'),
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default="Ordering")
    charge_id = models.CharField(max_length=200, null=True, default='')

    email = models.EmailField(max_length=200, null=True, validators=[validate_email])
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=11, null=True)
    instructions = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class Gallery(models.Model):
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return str(self.id)
    
    @property
    def image1URL(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url
    def image2URL(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    def image3URL(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url
    def image4URL(self):
        try:
            url = self.image4.url
        except:
            url = ''
        return url

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Return(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Returned', 'Returned'),
    )

    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default="Pending")

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    fname = models.CharField(max_length=200, null=False)
    lname = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=11, null=False)
    instructions = models.TextField(max_length=500, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)