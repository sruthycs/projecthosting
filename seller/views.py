from django.shortcuts import render
from django.shortcuts import redirect
from dairyapp.forms import CustomUserCreationForm
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, request
from . models import *
from django.contrib import auth,messages
from django.contrib.auth.models import User
from hashlib import sha256
import stripe
from django.views import View
from dairyapp.models import Products,Services
from dairyapp.models import Cart,wishlist,Profile,user_address,categories
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.db.models import Q
from dairyapp.views import Seller_registration,categories
# Create your views here.

def sellerhome(request):
    user = request.session['id']
    print(user)
    sr= Products.objects.filter(myuser_id=user)
    catagory=categories.objects.all()
    print(sr)
    context={'sr':sr,'catagory':catagory}
    return render(request,"seller/index.html",context)



class ProductAdd(View):
    def post(self, request):
        user = request.session['id']
        print(user)
        Product_name = request.POST.get("pname")
        price = request.POST.get("pprice")
        quantity = request.POST.get("quantity")
        image = request.FILES.get("pimage")
        adddate = request.POST.get("adddate")
        expirydate = request.POST.get("expiry")
        category = request.POST.get("category")
        cata=categories.objects.filter(title=category).values('id').get()['id']
        cataid=categories.objects.get(id=cata)
        print(Product_name, price, quantity, image, adddate,category, expirydate)
        r = Products(prd_name=Product_name , prd_price=price, stock =quantity, prd_img=image,category=cataid, adddate=adddate,expirydate=expirydate,myuser_id=user)
        r.save()
        return HttpResponse("<script>alert('Product Added');window.location='sellerhome';</script>")
        return render(request, 'seller/index.html')


def shop(request):
    user = request.user
    dict_shp={
        'product':Products.objects.all()
    }


    return render(request,"shopping.html",dict_shp)

def sellerlogin():
  return redirect(request,"sellerhome")

class LoginPage(View):
    def post(self,request):
        # request.session['email'] = 'null'
        print("hello")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if Seller_registration.objects.filter(email=username, password=password,role="Seller").exists():
           login= Seller_registration.objects.filter(email=username,password=password)
           for admin in login:
                email=admin.email
                request.session['email']=admin.email
                request.session['password'] = admin.password
                request.session['first_name'] = admin.first_name
                request.session['last_name'] = admin.last_name
                request.session['role'] = admin.role
                request.session['phone_no'] = admin.phone_no
                request.session['id'] = admin.id
                print(email)
                customers = Seller_registration.objects.filter(role="Seller", status='active').values()
                count=customers.count()
                print(count)
                # return HttpResponse("<script>alert('login  Successfull');window.location=' sellerhome';</script>")
                return redirect('sellerhome')
        elif Seller_registration.objects.filter(email=username, password=password,role="Deliveryboy").exists():
            login = Seller_registration.objects.filter(email=username, password=password)
            for admin in login:
                email = admin.email
                request.session['email'] = admin.email
                request.session['password'] = admin.password
                request.session['first_name'] = admin.first_name
                request.session['last_name'] = admin.last_name
                request.session['role'] = admin.role
                request.session['phone_no'] = admin.phone_no
                request.session['id'] = admin.id
                print(email)
                customers = Seller_registration.objects.filter(role="Seller", status='active').values()
                count = customers.count()
                print(count)
                return redirect('productdelivery')
                # return HttpResponse("<script>alert('login  Successfull');window.location='/productdelivery';</script>")
        else:
            return HttpResponse("<script>alert('no username or email found');window.location='/sellerlogin';</script>")

class RemoveProduct(View):
    def post(self, request,id):

        print("remove item id",id)
        return redirect(request,"sellerhome")

def Edit(request):
    sr = Products.objects.filter(myuser_id=user)
    context = {'sr': sr}
    return redirect(request,'index.html',context)

def Update(request,id):
    if request.method == "POST":
        user=request.session['id']
        Product_name = request.POST.get("pname")
        price = request.POST.get("pprice")
        quantity = request.POST.get("quantity")
        image = request.FILES.get("pimage")
        product=Products.objects.get(id=id)
        product.prd_name=Product_name
        product.prd_price=price
        product.stock=quantity
        product.prd_img=image


        # r = Products(prd_name=Product_name, prd_price=price, stock=quantity, prd_img=image, adddate=adddate,
        #              expirydate=expirydate, myuser=user)
        product.save()
        return redirect('sellerhome')
    # return render(request, 'seller/index.html')

def DELETE(request,id):
    sr = Products.objects.filter(id=id)
    sr.delete()

    context = {'sr': sr}
    return redirect('sellerhome')

    # return redirect(request,'sellerhome')