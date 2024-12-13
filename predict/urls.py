
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('startregister/',views.startRegister,name='startregister'),
    path('processregister/',views.processRegister,name='processregister'),
    path('startlogin/',views.startLogin,name='startlogin'),
    path('processlogin/',views.processLogin,name='processlogin'),
    path('startaddpost/',views.startAddPost,name='startaddpost'),
    path('userhome/', views.userHome, name='user_home'),
    path('addpost/',views.addPost,name='addpost'),
]