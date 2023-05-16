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
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from django.core.mail import send_mail
from .models import ReviewRating, OrderPlaced

from .models import Products,Services
from dairyapp.models import Cart,wishlist,Profile,user_address
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
from django.shortcuts import render,redirect
from django.db.models import Q
stripe.api_key = settings.STRIPE_PRIVATE_KEY
def demo(request):
    return render(request,"home.html")

def live(request):
    return render(request,"live.html")
def sellerlogin(request):
    return render(request,"sellerlogin.html")
def nav(request):
    return render(request,"nav.html")
def index(request):
    return render(request,"seller/index.html")
def deliveryboy(request,id):
    print(id)
    myproduct=Products.objects.get(prd_name=id)

    return render(request,"deliveryboy.html",{'myproduct':myproduct})

def productdelivery(request):
        orders = OrderPlaced.objects.all()
        context = {'orders': orders}

        return render(request, 'productdelivery.html', context)

def dboy1(request):
    # Get all the undelivered orders and sort them by ID
    orders = OrderPlaced.objects.exclude(status='Delivered').order_by('id')

    # Get the active delivery boys and sort them by ID
    delivery_boys = User.objects.filter(role=deliveryboy, is_admin=False, is_active=True).order_by('id')

    # Divide the orders equally among all the delivery boys
    num_delivery_boys = delivery_boys.count()
    orders_per_delivery_boy = orders.count() // num_delivery_boys
    remaining_orders = orders.count() % num_delivery_boys

    # Create a list of orders for each delivery boy
    order_lists = [[] for _ in range(num_delivery_boys)]
    index = 0
    for i, order in enumerate(orders):
        if index < num_delivery_boys:
            order_lists[index].append(order)
            index += 1
        else:
            index = 0
            order_lists[index].append(order)
            index += 1

    # Assign orders to delivery boys in a round-robin fashion
    order_index = 0
    for i, delivery_boy in enumerate(delivery_boys):
        orders_to_assign = orders_per_delivery_boy
        if i < remaining_orders:
            orders_to_assign += 1
        for order in order_lists[order_index][:orders_to_assign]:
            order.delivery_boy = delivery_boy
            order.save()
        order_index = (order_index + 1) % num_delivery_boys

    # Get the orders for the current delivery boy
    delivery_boy_orders = OrderPlaced.objects.filter(delivery_boy=request.user)

    context = {
        'orders': delivery_boy_orders,
    }

    return render(request, 'dboy1.html', context)

def dboy2(request, id):
    # dboy = OrderPlaced.objects.filter(id=id),values('id').get()['id']
    # print(dboy,"$$$$$$$$$$$$$$$$$$$")
    orders = OrderPlaced.objects.filter(id=id)
    order = get_object_or_404(OrderPlaced, id=id, status='Pending')
    print(order.status)
    print(order.otp)
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        print(entered_otp)
        if entered_otp == OrderPlaced.otp:
            order.status = 'Delivered'
            order.is_ordered = True
            order.save()
            print(order.status)
            return redirect('sellerhome')
        else:
          messages.success(request, 'Invalid OTP. ')
    return HttpResponse("<script>alert('Your Product has been delivered');window.location='/productdelivery';</script>")
    return render(request, 'thanks.html', {'order': order,'orders': orders})


def CUSTOMERORDER(request):
    user = request.user
    order = OrderPlaced.objects.filter(product_user=user)
    product = Products.objects.all()
    context = {'order': order,'product':product}

    return render(request,"seller/custemerorder.html",context)






def singleview(request,id):
    product = Products.objects.get(id=id)
    review = ReviewRating.objects.filter(product_id=id)
    context = {
        'product' : product,
        'review':review
    }
    return render(request,"singleview.html",context)

def deliveryboylogin(request):
    return render(request,"deliveryboylogin.html")

def wishlists(request):
    return render(request,'wishlist.html')
def review(request):
    return render(request,'review.html')

def checkout(request):
    return render(request,"checkout.html")

# def saveEnquiry(request):
#     if request.method == 'POST':
#         phone = request.POST.get['phone']
#         address = request.POST.get['address']
#         city = request.POST.get['city']
#         state = request.POST.get['state']
#         country = request.POST.get[' country']
#         pincode = request.POST.get['pincode']
#         en=Profile(phone=phone,address=address,city=city,state=state, country= country,pincode=pincode)
#         en.save()
#     return render(request,"checkout.html")

@login_required(login_url='login')
def shipping_address(request):
    if request.method=='POST':
        fname=request.POST.get('fname');
        lname=request.POST.get('lname');
        email=request.POST.get('email');
        phone = request.POST.get('phone');
        hname = request.POST.get('hname');
        street = request.POST.get('street');
        city = request.POST.get('city');
        district = request.POST.get('district');
        pin = request.POST.get('pin');
        user = request.user.id
        address=user_address(user=request.user,user_id=user,fname=fname,lname=lname,email=email,phone_no=phone,hname=hname,street=street,city=city,district=district,pin=pin)
        address.save()
        messages.success(request, 'Shipping Address Added Successfully...')
        add = user_address.objects.filter(user=request.user)
        dict_shp = {
            'address': add
        }

        return render(request, "payment.html", dict_shp)
    return redirect('checkout')

@login_required(login_url='login')
def cart(request):
    user = request.user
    cart=Cart.objects.filter(user_id=user)
    total=0
    for i in cart:
        total += i.product.price * i.product_qty
    category=Category.objects.all()
    return render(request,'Cart.html',{'cart':cart,'total':total,'category':category})

# Add to Cart.
@login_required(login_url='login')
def addcart(request, id):
    user = request.user
    item = Products.objects.get(id=id)
    if int(item.stock) > 0:
        if Cart.objects.filter(user_id=user, product_id=item).exists():
            return redirect(cart)
        else:
            product_qty = 1
            price = item.prd_price * product_qty
            new_cart = Cart(user_id=user.id, product_id=item.id, product_qty=product_qty, price=price)
            new_cart.save()
            return redirect(cart)


#Cart Quentity Plus Settings
def plusqty(request, id):
    cart = Cart.objects.filter(id=id).first()
    if cart:
        if cart.product.stock > cart.product_qty:
            cart.product_qty += 1
            cart.price = cart.product_qty * cart.product.price
            cart.save()
            return redirect('cart')
        else:
            messages.error(request, 'Out of Stock')
    else:
        messages.error(request, 'Cart not found')
    return redirect('cart')


# Cart Quentity Plus Settings
def minusqty(request, id):
    cart = Cart.objects.filter(id=id)
    for cart in cart:
        if cart.product_qty > 1:
            cart.product_qty -= 1
            cart.price = cart.product_qty * cart.product.price
            cart.save()
            return redirect('cart')
        return redirect('cart')


# View Cart Page
@login_required(login_url='login')
def cart(request):
    user = request.user
    cart = Cart.objects.filter(user_id=user)
    total = 0
    for i in cart:
        total += i.product.prd_price * i.product_qty

    # subcategory = Subcategory.objects.all()
    return render(request, 'Cart.html',
                  {'cart': cart, 'total': total})


# Remove Items From Cart
def de_cart(request, id):
    Cart.objects.get(id=id).delete()
    return redirect(cart)

# def registration(request):
#     if request.method=='POST':
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         username = request.POST['username']
#         email=request.POST['email']
#         pwd1=request.POST['pwd1']
#         pwd2=request.POST['pwd2']
#
#
#         if pwd1==pwd2:
#             if register.objects.filter(email=email).exists():
#                 print("exists")
#                 return redirect('shopping')
#             else:
#                 register(first_name=first_name, last_name=last_name, username=username, email=email, pwd1=pwd1, pwd2=pwd2).save()
#                 login(email=email,pwd1=pwd1).save()
#                 print("reg")
#                 # return redirect('company/')
#                 return redirect('shopping')
#
#         else:
#             print("not match")
#             return redirect('login')
#     else:
#         return render(request,'register.html')
#
#
#
#


def Sellerregistration(request,role):
   print(role)
   return render(request, 'sellerregistration.html',{'role':role})
def deliveryboyregistration(request,role):
   print(role)
   return render(request, 'sellerregistration.html',{'role':role})

@login_required(login_url='login')
def add_wishlist(request,id):
    user = request.user
    item=Products.objects.get(id=id)
    if wishlist.objects.filter( user_id =user,product_id=item).exists():
        messages.success(request, 'Already in the wishlist ')
        return redirect('shopping')
    else:
            new_wishlist=wishlist(user_id=user.id,product_id=item.id)
            new_wishlist.save()
            messages.success(request, 'Product added to the wishlist ')
            return redirect('shopping')
    messages.success(request, 'Sign in..!!')
    return redirect(index)



@login_required(login_url='login')
def view_wishlist(request):
        user = request.user
        wish=wishlist.objects.filter(user_id=user)
        category=categories.objects.all()
        print(wish,category)

        return render(request,"wishlist.html",{'wishlist':wish,'category':category})



def de_wishlist(request,id):
    wishlist.objects.get(id=id).delete()
    return redirect('view_wishlist')



def shopping(request):
    dict_shp={
        'product':Products.objects.all()
    }


    return render(request,"shopping.html",dict_shp)
def service(request):
    services = Services.objects.all()

    return render(request,"service.html",{'service':services})

def payments(request):
    user = request.user
    cart = Cart.objects.filter(user_id=user)
    total = 0
    for i in cart:
        total += i.product.prd_price * i.product_qty
    total=int(total)*100
    print(total)
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency':'inr',
                'unit_amount':total,
                'product_data':{
                    'name':'your cart'
                },

            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('thanks'))+'?session_id = {CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('cart')),
    )
    context = {
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'user':user,
        'total':total
    }
    return render(request, 'payments.html', context)


def send_order_confirmation_email(order):
    otp_code = order.otp
    user = order.user
    email_body = render_to_string('order_confirmation_email.html', {'order': order, 'otp_code': otp_code})

    message = render_to_string('order_confirmation_email.html', {
        'user': user,
        'otp_code': otp_code,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'email_body': email_body
    })

    send_mail(
        'Order Confirmation and OTP',
        message,
        'bookrakbook@gmail.com',
        [user.email],
        fail_silently=False,
    )
# payment details
def thanks(request):
    user = request.user
    print("gggggggggggggggggggggggggggggg",user.id)
    myuser = User.objects.get(id=user.id)
    address = user_address.objects.get(user_id=user.id)
    cartitem= Cart.objects.filter(user_id=user)
    print(cartitem)

    print(cart)
    complete = "True"
    for i in cartitem:
        otp_code = str(random.randint(100000, 999999))
        order = OrderPlaced( user=myuser, complete=complete,otp=otp_code,myorder=address,product=i)
        order.save()
        send_order_confirmation_email(order)
    print(user, complete)
    return HttpResponse("Thank you for your order!")
    # for i in cartitem:
    #     otp_code = str(random.randint(100000, 999999))
    #     order = OrderPlaced(user=request.user, product=i.product,  otp=otp_code, is_ordered=True,complete=complete,myorder=address, product1=i )
    #     order.save()
    #     send_order_confirmation_email(order)
    #     # i.product.book_quantity -= i.product_qty
    #     i.product.save()
    #     i.delete()
    #
    # return redirect('thanks.html')
    #
    # return render(request, 'thanks.html', {'user': user})

def sellerlogin(request):
    return render(request,'sellerlogin.html')


def Submit(request,role):
    print("gggggggggggggggggggggggggggggggggggggggggggggggggg")
    if request.method=='POST':
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone")
        password = request.POST.get("pass")
        if role == "Seller":
            status="inactive"
            print(first_name, last_name, email, phone_no, password, role, status)

            if not Seller_registration.objects.filter(email=email).exists():
                print("Not exist")

                # val.user_id = Registration.objects.get()
                # val.first_name = first_name

                r = Seller_registration(first_name=first_name, last_name=last_name, phone_no=phone_no, role=role, status=status,email=email,password=password)
                r.save()
                # val.password = password
                # val.email = email
                # val.user_id_id = r.id
                # print(val.email, val.password,val.user_id_id)
                # val.save()

                print(first_name, last_name, email, phone_no, password, role, status,email,password)
                return HttpResponse("<script>alert('Your Account has  created');window.location='/sellerlogin';</script>")
                return render(request, 'home/home.html', {'role': role})
            else:
                return HttpResponse("<script>alert('Email Id already Exist');window.location='//';</script>")
        if role == "Deliveryboy":
            status = "inactive"
            print(first_name, last_name, email, phone_no, password, role, status)

            if not Seller_registration.objects.filter(email=email).exists():
                print("Not exist")

                # val.user_id = Registration.objects.get()
                # val.first_name = first_name

                r = Seller_registration(first_name=first_name, last_name=last_name, phone_no=phone_no, role=role,
                                        status=status, email=email, password=password)
                r.save()
                # val.password = password
                # val.email = email
                # val.user_id_id = r.id
                # print(val.email, val.password,val.user_id_id)
                # val.save()

                print(first_name, last_name, email, phone_no, password, role, status, email, password)
                return HttpResponse(
                    "<script>alert('Your Account has  created');window.location='/sellerlogin';</script>")
                return render(request, 'home/home.html', {'role': role})
            else:
                return HttpResponse("<script>alert('Email Id already Exist');window.location='//';</script>")
def signup(request):
    return render(request,'signup.html')
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email,
                                                password=password)
                user.save();
                print("user Created")
                messages.success(request, "Account Created Successfully")
        else:
            print("password not match")
            messages.info(request, "Password incorrect")
            return redirect('register')
        return redirect('login')
    return render(request, "register.html")

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('live')
        else:
            messages.info(request, "Invalid credentials")
            return redirect('login')
    return render(request, "login.html")




def SearchResult(request):
    products=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        products=Products.objects.all().filter(Q(prd_name__contains=query) | Q(prd_description__contains=query))
        return render(request,'search.html',{'query':query,'products':products})

def PRODUCT_DETAIL_PAGE(request):
    return render(request,'product_single.html')
# def reviewss(request, id):
#         if request.method == 'POST':
#             try:
#                 reviews = ReviewRating.objects.get(user_id=request.user.id, product_id=id)
#                 subject = request.POST.get('subject')
#                 rating = request.POST.get('rating')
#                 review = request.POST.get('review')
#                 reviews.subject = subject
#                 reviews.rating = rating
#                 reviews.review = review
#                 reviews.save()
#                 print(reviews)
#                 messages.success(request, 'Thank you! Your review has been updated.')
#                 return redirect(request.META.get('HTTP_REFERER'))
#             except ReviewRating.DoesNotExist:
#                 subject = request.POST.get('subject')
#                 rating = request.POST.get('rating')
#                 review = request.POST.get('review')
#                 data = ReviewRating()
#                 data.subject = subject
#                 data.rating = rating
#                 data.review = review
#                 data.ip = request.META.get('REMOTE_ADDR')
#                 data.product_id = id
#                 data.user_id = request.user.id
#                 if OrderPlaced.objects.filter(user_id=request.user.id, id=id, complete=True).exists():
#                     data.save()
#                     print(data)
#                     messages.success(request, 'Thank you! Your review has been submitted.')
#                     return redirect(request.META.get('HTTP_REFERER'))
#                 else:
#                     messages.warning(request, 'You can only review products that you have purchased.')
#                     return redirect(request.META.get('HTTP_REFERER'))
#         else:
#             return redirect('/')



def reviewss(request, id):
        if request.method == 'POST':
                print("hai")
                subject = request.POST.get('subject')
                rating = request.POST.get('rating')
                review = request.POST.get('review')
                data = ReviewRating()
                data.subject = subject
                data.rating = rating
                data.review = review
                print(data.subject,data.rating,data.review)
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = id
                data.user_id = request.user.id
                user= request.user.id
                review = ReviewRating.objects.filter(product_id=id)
                product = Products.objects.get(id=id)
                if not ReviewRating.objects.filter(user_id=user).exists():
                    if OrderPlaced.objects.filter(user_id=user, product_id__product_id__id=id, complete=True).exists():
                        data.save()
                        print(data)
                        return render(request, 'singleview.html', {'review': review, 'product' : product})
                        return HttpResponse("<script>alert('Email Id already Exist');window.location='//';</script>")
                        messages.success(request, 'Thank you! Your review has been submitted.')
                        return redirect(request.META.get('HTTP_REFERER'))
                    else:
                        return HttpResponse("<script>alert('Email Id is not already Exist');window.location='//';</script>")
                        messages.warning(request, 'You can only review products that you have purchased.')
                        return redirect(request.META.get('HTTP_REFERER'))
                else:
                    return render(request,'singleview.html',{'review': review, 'product' : product})

        else:
            return redirect('/')

 # pdf generate code
import csv
def order_detailslog(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_details.csv"'
    writer = csv.writer(response)
    writer.writerow(['user', 'ordered_date','product'])
    order_details = OrderPlaced.objects.all().values_list('user', 'ordered_date','product')
    for i in order_details:
        writer.writerow(i)
    return response
# My Reviews

def my_reviews(request):
     reviews=ProductReview.objects.filter(user=request.user).order_by('id')
     return render(request, 'user/reviews.html', {'reviews': reviews})



def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')
 