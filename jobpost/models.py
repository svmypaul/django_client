from django.db import models

# Create your models here.

class uniqueids(models.Model):

    uniqueid = models.CharField(max_length = 20)

class CompanyLogin(models.Model):
    company_name = models.CharField(max_length=100)
    company_address = models.TextField()
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    password = models.TextField()  # Assuming hashed password will be stored
    unique_id = models.CharField(max_length=100)



class recruiter_login(models.Model):

    uniqueid = models.CharField(max_length = 20)
    company_name = models.CharField(max_length = 30)
    name = models.CharField(max_length = 30)
    username = models.CharField(max_length = 20)
    mail = models.CharField(max_length = 30)
    psw = models.TextField()
    dob = models.DateField()


class gmail_cv(models.Model):

    time = models.DateField()
    mail = models.CharField(max_length = 30)
    name = models.CharField(max_length = 30)
    heading = models.TextField()
    body = models.TextField()
    skill = models.TextField()
    contact_no = models.CharField(max_length = 20)
    contact_mail = models.CharField(max_length = 20)
    address = models.TextField()
    company_name = models.CharField(max_length = 30)
    recruiter_name = models.CharField(max_length = 30)
    filename = models.CharField(max_length = 30)
    uniqueid = models.CharField(max_length = 20)