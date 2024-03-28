from django.shortcuts import render
from jobpost.modul import generate_random_id, authorize, exchange_code_for_token
from jobpost.models import uniqueids, CompanyLogin, recruiter_login, gmail_cv
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from django.conf import settings
import googleapiclient.discovery
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def home(request):

    if 'username' in request.session:
        username = request.session['username']
        return render(request, 'index.html',{'username': username})

    return render(request, 'index.html')

def login_reg(request):

    if 'username' in request.session:
        username = request.session['username']
        return render(request, 'index.html',{'username': username})
    
    return render(request, 'login_reg.html')

def company_register(request):
    
     if request.method == "POST":
        
        company_name = request.POST.get('company-name')
        company_add = request.POST.get('company-address')
        username = request.POST.get('username')
        mail = request.POST.get('email')
        psw = request.POST.get('pwd')
        cnf_pwd = request.POST.get('cnf-psw')
        uniqueid = generate_random_id()

        try:
            existing_username = CompanyLogin.objects.values_list('username', flat=True)
            existing_mail = CompanyLogin.objects.values_list('mail', flat=True)
            existing_username = []
            existing_mail = []
        except:
            existing_username = []
            existing_mail = []
            pass
        if psw != cnf_pwd:
            
            return render(request, 'login_reg.html',{'messages': "The input for the password and confirm password fields must match exactly"})
        
        elif (username in existing_username) or (mail in existing_mail):

            return render(request, 'login_reg.html',{'messages': "This  username or email is already exist please different username or email"})
        else:

            hash_psw = make_password(psw)
            v = f"{company_name} {company_add} {username} {mail} {hash_psw} {cnf_pwd} "
            print(v)
            b1 = uniqueids(uniqueid = uniqueid)
            b2 = CompanyLogin(company_name = company_name, company_address = company_add,username=username,email=mail,password=hash_psw,unique_id=uniqueid)

            b1.save()
            b2.save()
            return render(request, 'test.html',{'result': v})
        
     elif 'username' in request.session:
        username = request.session['username']
        return render(request, 'index.html',{'username': username})
     
     else:
         return render(request, 'login_reg.html')
     

def company_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        psw = request.POST.get('psw')
        
        user = CompanyLogin.objects.filter(username=username)
        if user.exists():

            passwordentered = user.values('password')[0]['password']
            
            if check_password(psw, passwordentered):

                request.session['username'] = username
                return render(request, 'index.html',{'username': username})
            else:
               return render(request, 'login_reg.html',{'messages': "Wrong Password"}) 
        else:
            return render(request, 'login_reg.html',{'messages': "Wrong username"})
        
    elif 'username' in request.session:
        username = request.session['username']
        return render(request, 'index.html',{'username': username})

    else:
         return render(request, 'login_reg.html')

def recruiter_register(request):
    
     if request.method == "POST":
        
        company_id = request.POST.get("companyid")
        name = request.POST.get('name')
        username = request.POST.get('username')
        mail = request.POST.get('email')
        psw = request.POST.get('psw')
        cnf_pwd = request.POST.get('cnf-psw')
        month = request.POST.get('month')
        day = request.POST.get('day')
        year = request.POST.get('year')

        company_id_list = CompanyLogin.objects.values_list('unique_id', flat=True)
        dob_str = f"{year}-{month}-{day}"

        # Parse the date string into a datetime object
        date_obj = datetime.strptime(dob_str, "%Y-%B-%d")

        # Format the datetime object into MySQL date format
        dob = date_obj.strftime("%Y-%m-%d")
        try:
            existing_username = recruiter_login.objects.values_list('username', flat=True)
            existing_mail = recruiter_login.objects.values_list('mail', flat=True)
        except:
            existing_username = []
            existing_mail = []
            pass
        if psw != cnf_pwd:
            
            return render(request, 'login_reg.html',{'messages': "The input for the password and confirm password fields must match exactly"})
        
        elif (username in existing_username) or (mail in existing_mail):

            return render(request, 'login_reg.html',{'messages': "This  username or email is already exist please different username or email"})
        
        elif company_id not in company_id_list:

            return render(request, 'login_reg.html',{'messages': "Invalid User id"})
        
        else:
            company_details = CompanyLogin.objects.filter(unique_id=company_id)
            print(company_details)

            first_company = company_details.first()
            company_name = first_company.company_name

            hash_psw = make_password(psw)
            v = f"{company_id} {name} {username} {mail} {hash_psw} {cnf_pwd} {company_name}"
            print(v)
            
            b2 = recruiter_login(company_name = company_name,name = name, username=username,mail=mail,psw=hash_psw,uniqueid=company_id,dob = dob)

            b2.save()
            return render(request, 'test.html',{'result': v})
        
     elif 'username' in request.session:
        username = request.session['username']
        return render(request, 'index.html',{'username': username})
     
     else:
         return render(request, 'login_reg.html')
     

def recruiter_Login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        psw = request.POST.get('psw')
        
        user = recruiter_login.objects.filter(username=username)
        if user.exists():

            passwordentered = user.values('psw')[0]['psw']
            company_name = user.values('company_name')[0]['company_name']
            uniqueid = user.values('uniqueid')[0]['uniqueid']
            mailid = user.values('mail')[0]['mail']
            
            if check_password(psw, passwordentered):

                request.session['username'] = username
                request.session['company_name'] = company_name
                request.session['uniqueid'] = uniqueid
                request.session['mailid'] = mailid
                # return redirect(f'http://localhost:8080/?username={username}')
                return render(request, 'recruiter_dashboard.html',{'username': username,'companyname': company_name, 'uniqueid': uniqueid, 'mailid': mailid})
                # return render(request, 'recruiter_dashboard.html')
            else:
               return render(request, 'login_reg.html',{'messages': "Wrong Password"}) 
        else:
            return render(request, 'login_reg.html',{'messages': "Wrong username"})
        
    elif 'username' in request.session:
        username = request.session['username']
        return render(request, 'index.html',{'username': username})

    else:
         return render(request, 'login_reg.html')
    
def logout(request):

    if 'username' in request.session:

        del request.session['username']
        del request.session['company_name']
        del request.session['uniqueid']
        del request.session['mailid']

        return render(request, 'index.html')
    
    return render(request, 'index.html')

def recruiter_dashboard(request):

    if 'username' in request.session:
        username = request.session['username']
        company_name = request.session['company_name']
        uniqueid =  request.session['uniqueid']
        mailid = request.session['mailid']

        user_data = gmail_cv.objects.filter(recruiter_name=username)
        
        mail_json = user_data.values_list('mail', flat=True)
        name_json = user_data.values_list('name', flat=True)
        datetime_json = user_data.values_list('time', flat=True)
        filename_json = user_data.values_list('filename', flat=True)
        skill_json = user_data.values_list('skill', flat=True)
        data = zip(mail_json, name_json, datetime_json, filename_json, skill_json)
        return render(request, 'recruiter_dashboard.html',{'username': username,'companyname': company_name, 'uniqueid': uniqueid, 'mailid': mailid,"data": data})
    else:
        return render(request, 'index.html')

# def parser(request):

#     if 'username' in request.session:

#     else:
#         return render(request, 'login_reg.html')