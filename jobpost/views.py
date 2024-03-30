from django.shortcuts import render
from jobpost.modul import generate_random_id, is_valid_email, replace_placeholders, send_email
from jobpost.models import uniqueids, CompanyLogin, recruiter_login, gmail_cv, posted_jobs
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
            company_name = user.values('company_name')[0]['company_name']
            uniqueid = user.values('unique_id')[0]['unique_id']
            mailid = user.values('email')[0]['email']
            
            if check_password(psw, passwordentered):

                request.session['username'] = username
                request.session['company_name'] = company_name
                request.session['uniqueid'] = uniqueid
                request.session['mailid'] = mailid

                request.session['logintype'] = "company"
                # return render(request, 'index.html',{'username': username})
                return redirect(reverse('dashboard'))
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
                request.session['logintype'] = "recruiter"
                # return redirect(f'http://localhost:8080/?username={username}')
                # return render(request, 'recruiter_dashboard.html',{'username': username,'companyname': company_name, 'uniqueid': uniqueid, 'mailid': mailid})
                return redirect(reverse('dashboard'))
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

def dashboard(request):

    login_type = request.session['logintype']

    if login_type == "company":
        return redirect(reverse('company-dashboard'))
    
    elif login_type == "recruiter":
        return redirect(reverse('recruiter-dashboard'))
    
    else:
        return redirect(reverse('home'))

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
        id_json = user_data.values_list('id', flat=True)

        data = zip(mail_json, name_json, datetime_json, filename_json, skill_json , id_json)
        return render(request, 'recruiter_dashboard.html',{'username': username,'companyname': company_name, 'uniqueid': uniqueid, 'mailid': mailid,"data": data})
    else:
        return render(request, 'index.html')
    
def company_dashboard(request):

    if 'username' in request.session:
        username = request.session['username']
        company_name = request.session['company_name']
        uniqueid =  request.session['uniqueid']
        mailid = request.session['mailid']

        rec_user_data = recruiter_login.objects.filter(uniqueid=uniqueid)

        if rec_user_data.exists():

            name = rec_user_data.values_list('name', flat=True)
            mailid = rec_user_data.values_list('mail', flat=True)
            print(name)
            total_rec = len(name)
            rec_users = zip(name,mailid)
            return render(request, 'company_dashboard.html',{'username': username,'company_name': company_name,'uniqueid': uniqueid,'mailid':mailid,'total_rec': total_rec,'data': rec_users})
        
        else:
            return render(request, 'company_dashboard.html',{'username': username,'company_name': company_name,'uniqueid': uniqueid,'mailid':mailid})
    else:
        return redirect(reverse('home'))

def jobpost(request):

    mailid = request.session.get('mailid')

    job_data = posted_jobs.objects.filter(mail=mailid)
        
    designation_json = job_data.values_list('designation', flat=True)
    time_json = job_data.values_list('time', flat=True)
    jobid_json = job_data.values_list('uniquejobid', flat=True)
        
    data = zip(designation_json, time_json, jobid_json)
    return render(request, 'jobpost.html',{'data':data})

def newjobpost(request):

    return render(request, 'newjobpost.html')

def preview(request):

    if request.method == "POST":
        # fetch data from form
        designation = request.POST.get('designation')
        skills = request.POST.getlist('skills[]')
        skills_string = ", ".join(skills)
        work_loc = request.POST.get('work-loc')
        hire_locs = request.POST.getlist('hire-loc[]')
        hire_locs_string = ", ".join(hire_locs)
        exp_from = request.POST.get('exp-from')
        exp_to = request.POST.get('exp-to')
        salary = request.POST.get('salary')
        job_des = request.POST.get('job-des')
        shift_time_from = request.POST.get('shift-time-from')
        shift_time_to = request.POST.get('shift-time-to')
        companyname = request.POST.get('companyname')
        rec_name = request.POST.get('rec-name')
        tel = request.POST.get('tel')
        telphon = f"+91{tel}"
        mail = request.POST.get('mail')
        gmail = f'{mail}@gmail.com'

        # Store the data in the session
        request.session['designation'] = designation
        request.session['skills'] = skills_string
        request.session['work_loc'] = work_loc
        request.session['hire_locs'] = hire_locs_string
        request.session['exp_from'] = exp_from
        request.session['exp_to'] = exp_to
        request.session['salary'] = salary
        request.session['job_des'] = job_des
        request.session['shift_time_from'] = shift_time_from
        request.session['shift_time_to'] = shift_time_to
        request.session['companyname'] = companyname
        request.session['rec_name'] = rec_name
        request.session['telphon'] = telphon
        request.session['gmail'] = gmail
        request.session['ind'] = "False"
        return render(request, 'preview.html',{'designation': designation,
                                                'skills': skills_string,
                                                'work_loc': work_loc,
                                                'hire_locs': hire_locs_string,
                                                'exp_from': exp_from,
                                                'exp_to': exp_to,
                                                'salary': salary,
                                                'job_des': job_des,
                                                'shift_time_from': shift_time_from,
                                                'shift_time_to': shift_time_to,
                                                'companyname': companyname,
                                                'rec_name': rec_name,
                                                'tel': telphon,
                                                'gmail': gmail,
                                            })
    else:
        return redirect(reverse('newjobpost'))
        

def savejobpost(request):

    # Retrieve all data from the session
    designation = request.session.get('designation')
    skills = request.session.get('skills')
    work_loc = request.session.get('work_loc')
    hire_locs = request.session.get('hire_locs')
    exp_from = request.session.get('exp_from')
    exp_to = request.session.get('exp_to')

    exp = f'{exp_from} - {exp_to}'

    salary = request.session.get('salary')
    job_des = request.session.get('job_des')
    shift_time_from = request.session.get('shift_time_from')
    shift_time_to = request.session.get('shift_time_to')

    shift_time = f'{shift_time_from} - {shift_time_to}'

    companyname = request.session.get('companyname')
    rec_name = request.session.get('rec_name')
    telphon = request.session.get('telphon')
    gmail = request.session.get('gmail')
    mailid = request.session.get('mailid')
    uniqueid = request.session.get('uniqueid')
    current_time = datetime.now()


    num = 0
    jobpost_uniqueid = f'{uniqueid}job{num}'
    # print(designation, mailid, current_time,skills, work_loc ,uniqueid, hire_locs, exp, salary, job_des, shift_time, companyname, rec_name, telphon, gmail)
    job_data = posted_jobs.objects.filter(uniqueid=uniqueid)
    total_job = len(job_data)  # Count of rows in the queryset

    if total_job == 0:  # Check if there are no jobs with this uniqueid
        num = 1
    else:
        num = total_job + 1

    jobpost_uniqueid = f'{uniqueid}job{num}'

    if request.session.get('ind') == 'True':

        return render(request, 'successful.html',{'result': "You have already submited this job"})
    else:
        # Attempt to retrieve the job with the uniquejobid
        job_instance, created = posted_jobs.objects.get_or_create(uniquejobid=jobpost_uniqueid, defaults={
            'time': current_time,
            'mail': mailid,
            'designation': designation,
            'skills': skills,
            'work_loc': work_loc,
            'hire_locs': hire_locs,
            'exp': exp,
            'sallary': salary,
            'job_des': job_des,
            'shift_time': shift_time,
            'contact_no': telphon,
            'contact_mail': gmail,
            'job_address': work_loc,
            'company_name': companyname,
            'recruiter_name': rec_name,
            'uniqueid': uniqueid
        })

        # If the job was created, save it to the database
        if created:
            job_instance.save()

        request.session['ind'] = 'True'

        return render(request, 'successful.html',{'result': "Job posting successful!"})


def jobdetails(request):

    if request.method == "POST":
        # fetch data from form
        jobid = request.POST.get('jobid')
        print(jobid)
        # posted job details
        job_data = posted_jobs.objects.get(uniquejobid=jobid)
        print(job_data)
        designation = job_data.designation
        company_name = job_data.company_name
        recruiter_name = job_data.recruiter_name
        time = job_data.time
        skill = job_data.skills
        uniqueid = job_data.uniqueid
        job_skill =skill.split(', ')

        request.session['designation'] = designation
        request.session['company_name'] = company_name
        request.session['recruiter_name'] = recruiter_name

        # candidate's resume details
        gmail_cvs = gmail_cv.objects.filter(uniqueid=uniqueid)

        # Now you can use gmail_cv to get the skill_json
        can_skill_json = gmail_cvs.values_list('skill', flat=True)
        can_mail_json = gmail_cvs.values_list('contact_mail', flat=True)
        can_tel_json = gmail_cvs.values_list('contact_no', flat=True)
        can_name_json = gmail_cvs.values_list('name', flat=True)

        mail_list = []
        tel_list = []
        can_name_list = []
        for skill in job_skill:
            for i in range(len(can_skill_json)):  
                if skill in can_skill_json[i]:
                    mail_list.append(can_mail_json[i])
                    tel_list.append(can_tel_json[i])
                    can_name_list.append(can_name_json[i])
        
        request.session['fit_can_mail_list'] = mail_list
        request.session['fit_can_tel_list'] = tel_list
        request.session['fit_can_name_list'] = can_name_list
        return render(request, 'fit_can.html',{'total_can': max(len(mail_list),len(tel_list))})
    

def mailtemplate(request):
    return render(request, 'gmail_temp.html')

def sendmail(request):
    if request.method == "POST":
        temp = request.POST.get('textarea')

        mail_list = request.session.get('fit_can_mail_list')
        name_list = request.session.get('fit_can_name_list')

        result = ''
        for mail, name in zip(mail_list,name_list):
            print(mail)
            if is_valid_email(mail):
                companyname = request.session.get('company_name')
                recruitername = request.session.get('recruiter_name')
                designation = request.session.get('designation')

                text = replace_placeholders(temp,candidate_name = name,
                                            recruiter_name = recruitername,
                                            designation = designation,
                                            company_name = companyname,
                                            line_break = "<br>")
                subject =  "Vaccancy"
                body = text
                recipients = mail
                sender = "shubhamoy.svmy@gmail.com"
                password = "gpjhornymjapckrq"
                result = send_email(subject, body, sender, recipients, password)
        
        return render(request, 'successful copy.html',{'result': result})


def remove_can(request):
    if 'id' in request.GET:
        can_id = request.GET['id']
        print(can_id)
        cv_to_delete = gmail_cv.objects.get(id=can_id)

        # Delete the object
        cv_to_delete.delete()
    return redirect(reverse('recruiter-dashboard'))
    