from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views
from seller.views import ProductAdd


urlpatterns = [
    path('',views.demo,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('live',views.live,name='live'),
    path('nav',views.nav,name='nav'),
    path('singleview/<int:id>/', views.singleview, name='singleview'),
    path('payments',views.payments,name='payments'),
    path('shopping', views.shopping, name='shopping'),
    path('service', views.service, name='service'),
    path('review', views.review, name='review'),
    path('reviewss/<int:id>/', views.reviewss, name='reviewss'),
    path('signup', views.signup, name='signup'),
    path('sellerlogin', views.sellerlogin, name='sellerlogin'),
    path('product_details/',views.PRODUCT_DETAIL_PAGE,name='product_detail'),
    path('index', views.index, name='index'),

    path('productdelivery', views.productdelivery, name='productdelivery'),
    path('custemerorder/', views.CUSTOMERORDER, name='custemerorder'),

    path('my_reviews', views.my_reviews, name='my_reviews'),
    path('deliveryboy/<id>', views.deliveryboy, name='deliveryboy'),
    path('dboy2/<int:id>/', views.dboy2, name='dboy2'),

    path('send_order_confirmation_email/', views.send_order_confirmation_email, name='send_order_confirmation_email'),

    path('deliveryboyregistration', views.deliveryboyregistration, name='deliveryboyregistration'),
    path('Sellerregistration/<str:role>', views.Sellerregistration, name='Sellerregistration'),
    path('Sellerregistration/Submit/<str:role>', views.Submit, name='Submit'),
    path('cart/', views.cart, name='cart'),
    path('ProductAdd', ProductAdd.as_view(), name='ProductAdd'),
    path('addcart/<int:id>/', views.addcart, name='addcart'),
    path('de_cart/<int:id>/', views.de_cart, name='de_cart'),
    path('plusqty/<int:id>/',views.plusqty,name='plusqty'),
    path('minusqty/<int:id>/',views.minusqty,name='minusqty'),
    path('checkout/', views.checkout, name='checkout'),
    path('search',views.SearchResult,name='SearchResult'),

  

    path('shipping_address/', views.shipping_address, name='shipping_address'),
    path('wishlists/', views.wishlists, name='wishlists'),
    path('add_wishlist/<int:id>/',views.add_wishlist,name='add_wishlist'),
    path('view_wishlist',views.view_wishlist,name='view_wishlist'),
    path('de_wishlist/<int:id>/',views.de_wishlist,name='de_wishlist'),
    path('logout', views.logout, name='logout'),
####reset password urls####
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/login/',views.login,name='login'),
]