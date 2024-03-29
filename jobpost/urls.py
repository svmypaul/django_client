from django.contrib import admin
from django.urls import path, include
from jobpost import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home, name = "home"),
    path("login-reg/", views.login_reg, name="login-reg"),
    path("company-reg/", views.company_register, name="company-reg" ),
    path("company-login/", views.company_login, name="company-login" ),
    path("recruiter-reg/", views.recruiter_register, name="recruiter-reg" ),
    path("recruiter-login/", views.recruiter_Login, name="recruiter-login" ),
    path("logout/", views.logout, name="logout" ),
    path("recruiter-dashboard/", views.recruiter_dashboard, name="recruiter-dashboard" ),
    path('/jobpost', views.jobpost, name="jobpost"),
    path('/newjobpost', views.newjobpost, name="newjobpost"),
    path('/preview', views.preview, name="preview"),
    path('/savejobpost', views.savejobpost, name="savejobpost"),
    path('/jobdetails', views.jobdetails, name="jobdetails"),
    path('mailtemplate/', views.mailtemplate, name="mailtemplate"),
    path('sendmail/', views.sendmail, name="sendmail"),
    path('removecan/', views.remove_can, name="remove_can"),

    
]