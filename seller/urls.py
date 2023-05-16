from django.urls import path, include

from . import views
from.views import ProductAdd,LoginPage,RemoveProduct
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('/ProductAdd', ProductAdd.as_view(), name='ProductAdd'),
    path('/RemoveProduct/<id>', RemoveProduct.as_view(), name='RemoveProduct'),
    path('edit',views.Edit,name='edit'),
    path('/update/<str:id>',views.Update,name='update'),
    path('/sellerhome',views.sellerhome,name='sellerhome'),
    path('/LoginPage',LoginPage.as_view(), name='LoginPage'),
    path('/delete/<str:id>',views.DELETE,name='delete'),

]