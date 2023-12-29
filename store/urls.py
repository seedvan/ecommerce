from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name ='cart'),
    path('checkout/', views.checkout, name ='checkout'),
    path('update_item/', views.updateItem, name="updateItem"),
    path('process_order/', views.processOrder, name="process_order"),
    path('signup/', views.signup, name = 'signup'),
    #path('login/', views.login, name="login"),
    path('product/<int:pk>/', views.productdetails, name="product"),
    path('', include("django.contrib.auth.urls")),
    path('search/', views.search, name="search"),
    path('profile/', views.profile, name="profile"),
]