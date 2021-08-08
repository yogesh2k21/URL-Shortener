from django.contrib import admin
from django.urls import path
from urlhandler.views import home,contact,price,dash,generate
from authentication.views import login, signup, logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('login/',login,name="login"),
    path('logout/',logout,name='logout'),
    path('signup/',signup,name='signup'),
    path('contact/',contact,name='contact'),
    path('price/',price,name='price'),
    path('dash/',dash,name='dash'),
    path('generate/',generate,name='generate'),
    path('<str:query>/',home,name='home'),
]
