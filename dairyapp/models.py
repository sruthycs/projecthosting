# from statistics import mode
from django.db import models
from django.contrib.auth.models import User
import uuid
import random
# Create your models here.
#
class Review(models.Model):
    date = models.DateField()
    Description = models.CharField(max_length=200)
    rating = models.CharField(max_length=5)


class Address(models.Model):
    address = models.CharField(max_length=200)
    dob = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    pin = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    user_idproof = models.ImageField(upload_to =  None)
    image = models.ImageField(upload_to = None)



class categories(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to='cat-photo')

    def __str__(self):
        return self.title



class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    state = models.CharField(max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=50,null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Services(models.Model):
    name=models.CharField(max_length=100)
    img=models.ImageField(upload_to='Products')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class user_address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Email')
    fname = models.CharField(max_length=200,verbose_name='First Name')
    lname = models.CharField(max_length=200,verbose_name='Last Name')
    phone_no = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    hname = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    district=models.CharField(max_length=200)
    pin=models.CharField(max_length=200)

    def __str__(self):
        return self.fname

class Seller_registration(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_no = models.IntegerField( default=uuid.uuid1)
    role = models.CharField(max_length=200)
    status = models.CharField(max_length=200,default="inactive")
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, max_length=100, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, max_length=100, null=True)


class Products(models.Model):
    prd_name=models.CharField(max_length=100)
    prd_price=models.FloatField()
    prd_description = models.TextField()
    category = models.ForeignKey(categories,on_delete=models.CASCADE, max_length=100, null=True)
    stock = models.IntegerField(default=1)
    prd_img=models.ImageField(upload_to='Products')
    adddate = models.DateField("adddate", auto_now_add=True)
    expirydate = models.DateField("expirydate", null=True)
    myuser = models.ForeignKey(Seller_registration, on_delete=models.CASCADE, max_length=100, null=True)
    def __str__(self):
        return self.prd_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])


class ReviewRating(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_qty = models.IntegerField(default=1)
    price = models.IntegerField(default=0,null=True,blank=True)

    def get_product_price(self):
        price = [self.product.price]
        return sum(price)

class wishlist(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     product = models.ForeignKey(Products, on_delete=models.CASCADE)
     price = models.DecimalField(max_digits=20, decimal_places=2, default=0)


class OrderPlaced(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Received', 'Received'),
        ('Shipped', 'Shipped'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),

    )
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank =True)
    myorder = models.ForeignKey(user_address, on_delete=models.SET_NULL,null=True,blank =True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True,blank =True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    otp = models.CharField(max_length=6, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.otp:
            self.otp = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

#
#
#     class Meta:
#         db_table="registration"
# #
# # class login_details(models.Model):
# #     email = models.CharField(max_length=20)
# #     password = models.CharField(max_length=30)
# # class login_details(models.Model):
# #     email = models.CharField(max_length=200)
# #     password = models.CharField(max_length=200)
#
# class login(models.Model):
#     email=models.CharField(max_length=200)
#     pwd1=models.CharField(max_length=200)
#     class Meta:
#         db_table="login"
