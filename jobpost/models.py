from django.db import models

# Create your models here.

class uniqueids(models.Model):

    uniqueid = models.CharField(max_length = 20)

class CompanyLogin(models.Model):
    company_name = models.CharField(max_length=100)
    company_address = models.TextField()
    username = models.TextField()
    email = models.EmailField(max_length=254)
    password = models.TextField()  # Assuming hashed password will be stored
    unique_id = models.CharField(max_length=100)
    active = models.CharField(max_length=20)
    date = models.DateField()



class recruiter_login(models.Model):

    uniqueid = models.CharField(max_length=20)
    company_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    username = models.TextField()
    mail = models.TextField()
    psw = models.TextField()
    dob = models.DateField()
    rstat = models.CharField(max_length=30) 
    no_email = models.CharField(max_length=30)
    no_cv = models.CharField(max_length=30)

class gmail_cv(models.Model):

    time = models.DateField()
    mail = models.TextField()
    name = models.CharField(max_length = 30)
    heading = models.TextField()
    body = models.TextField()
    skill = models.TextField()
    contact_no = models.CharField(max_length = 20)
    contact_mail = models.TextField()
    address = models.TextField()
    company_name = models.CharField(max_length = 30)
    recruiter_name = models.CharField(max_length = 30)
    filename = models.CharField(max_length = 30)
    uniqueid = models.CharField(max_length = 20)


class posted_jobs(models.Model):

    time = models.DateField()
    mail = models.TextField()
    designation = models.CharField(max_length = 30)
    skills = models.TextField()
    work_loc = models.CharField(max_length = 30)
    hire_locs = models.CharField(max_length = 30)
    exp = models.CharField(max_length = 10)
    sallary = models.CharField(max_length = 20)
    job_des = models.TextField()
    shift_time = models.CharField(max_length = 10)
    contact_no = models.CharField(max_length = 20)
    contact_mail = models.CharField(max_length = 20)
    job_address = models.TextField()
    company_name = models.CharField(max_length = 30)
    recruiter_name = models.CharField(max_length = 30)
    uniquejobid = models.CharField(max_length = 20)
    uniqueid = models.CharField(max_length = 20)