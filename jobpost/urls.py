from django.contrib import admin
from django.urls import path, include
from jobpost import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home, name = "home"),
    path("login-reg/", views.login_reg, name="login-reg"),
    path("company-reg/", views.company_register, name="company-reg" ),
    path("company-login/", views.company_login, name="company-login" ),
    path("recuiter-reg/", views.recuiter_register, name="recuiter-reg" ),
    path("recuiter-login/", views.recuiter_Login, name="recuiter-login" ),
    path("logout/", views.logout, name="logout" ),
    
]