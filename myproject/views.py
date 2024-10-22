from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from myapp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q 

def base(req):
    return render (req, 'base.html')

def searchJob(req):
    
    query = req.GET.get('query')
    
    if query:
        
        data = JobModel.objects.filter(Q(job_title__icontains=query) 
                                       |Q(Job_Description__icontains=query) 
                                       |Q(Category__icontains=query))
    
    else:
        data = JobModel.objects.none()
        
    context={
        'data':data,
        'query':query
    }
    
    return render(req,"search.html",context)

def Table(req):
    data=JobModel.objects.all()

    context = {
        'data': data
    }
    return render(req,'Table.html',context)

def jobfeed(req):
    data=JobModel.objects.all()

    context = {
        'data': data
    }
    return render(req,'jobfeed.html',context)

def Addjob(req):
    current_user=req.user
    if current_user.user_type == "recruiters":
     if req.method=='POST':
        company_logo=req.FILES.get('company_logo')
        job_title=req.POST.get('job_title')
        Number_of_opening=req.POST.get('Number_of_opening')
        Category=req.POST.get('Category')
        Job_Description=req.POST.get('Job_Description')
        Skills=req.POST.get('Skills')

        books=JobModel(
            user=current_user,
            company_logo=company_logo,
            job_title=job_title,
            Number_of_opening=Number_of_opening,
            Category=Category,
            Job_Description=Job_Description,
            Skills=Skills,
        )
        books.save()
        return redirect('jobfeed')
    return render(req,'addjob.html')


def mainprofile(req,id):
    current_user=req.user

    Job=JobModel.objects.filter(id=id)
    text={
        'Job':Job,
    }
 
    return render(req,'mainprofile.html',text)

def deletejob(req,id):
    job=JobModel.objects.filter(id=id)
    job.delete()
    return redirect('Table')

def appliedjob(req):
    current_user=req.user
    if current_user.user_type == "recruiter":
        if req.method == 'POST':
            job=ApplyJobModel()
            job.user=current_user
            job.job_title=req.POST.get('job_title')
            job.company_type=req.POST.get('company_type')
            job.company_logo=req.FILES.get('company_logo')
            job.location=req.POST.get('location')
            job.company_name=req.POST.get('company_name')
            job.description=req.POST.get('description')
            job.salary=req.POST.get('salary')
            job.application_deadline=req.POST.get('application_deadline')
            job.posted_on=req.POST.get('posted_on')
            job.save()
            
            return redirect('jobfeed')

    return render(req, 'applyjob.html')

def editjob(req,id):
    current_user=req.user
    job=JobModel.objects.filter(id=id)

    if current_user.user_type == "recruiters":
     if req.method=='POST':
        company_logo=req.FILES.get('company_logo')
        job_title=req.POST.get('job_title')
        Number_of_opening=req.POST.get('Number_of_opening')
        Category=req.POST.get('Category')
        Job_Description=req.POST.get('Job_Description')
        Skills=req.POST.get('Skills')
        company_logo_old=req.POST.get('company_logo_old')

        user_object=Custom_user.objects.get(id=id)


        add=JobModel(
            id=id,
            user=user_object,
            job_title=job_title,
            Number_of_opening=Number_of_opening,
            Category=Category,
            Job_Description=Job_Description,
            Skills=Skills,
            )
        if company_logo:
          add.company_logo=company_logo
          add.save()
        else:
         add.company_logo=company_logo_old
         add.save()
        return redirect ('Table')

    return render (req,'editjob.html',{'job':job})

def password_change(req):
    current_user=req.user
    if req.method == 'POST':
        currentpassword = req.POST.get("currentpassword")
        newpassword = req.POST.get("newpassword")
        confirmpassword = req.POST.get("confirmpassword")

        if check_password(currentpassword,req.user.password):
            if newpassword==confirmpassword:
                current_user.set_password(newpassword)
                current_user.save()
                update_session_auth_hash(req,current_user)
                messages.success(req, "Your password has been changed successfully.")
                return redirect("loginpage")
            
            
            if newpassword != confirmpassword:
                messages.warning(req, "New passwords do not match")
                return redirect('password_change')
            else:
                messages.error(req, "Current password is incorrect")
                return render(req, "password.html")
            
    return render(req, 'password.html')


def loginpage(req):
    if req.method == 'POST':
        username = req.POST.get("username")
        password = req.POST.get("password")

        if not username or not password:
            messages.warning(req, "Both username and password are required")
            return render(req, "loginPage.html")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(req, user)
            messages.success(req, "Login Successfully")
            return redirect("base")
        else:
            messages.error(req, "Invalid username or password")

    return render(req, "login.html")


def registerpage(req):
    if req.method == 'POST':
        username = req.POST.get("username")
        Display_name = req.POST.get("Display_name")
        email = req.POST.get("email")
        user_type = req.POST.get("usertype")
        password = req.POST.get("password")
        confirm_password = req.POST.get("confirm_password")

        # Check for required fields
        if not all([username,Display_name, email, user_type,password, confirm_password]):
            messages.warning(req, "All fields are required")
            return render(req, "signupPage.html")

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(req, "Invalid email format")
            return render(req, "signupPage.html")

        # Check password confirmation
        if password != confirm_password:
            messages.error(req, "Passwords do not match")
            return render(req, "signupPage.html")

        # Password validation
        if len(password) < 4:
            messages.warning(req, "Password must be at least 8 characters long")
            return render(req, "signupPage.html")

        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            messages.warning(req, "Password must contain both letters and numbers")
            return render(req, "signupPage.html")

        # Create user
        try:
            user = Custom_user.objects.create_user(
                username=username,
                email=email,
                user_type=user_type,
                password=password,
            )
            if user_type=='jobseeker':
                viewersProfileModel.objects.create(user=user)
                
            elif user_type=='recruiters':
                CreatorProfileModel.objects.create(user=user)

            messages.success(req, "Account created successfully! Please log in.")
            return redirect("loginpage")
        except IntegrityError:
            messages.error(req, "Username or email already exists")
            return render(req, "signupPage.html")

    return render(req, "signupPage.html")

def logoutpage(req):
    logout(req)
    return redirect('loginpage')

#profile:


def Profile(req):
    current_user=req.user

    edu=CreatorProfileModel.objects.filter(user=current_user)
    exp=viewersProfileModel.objects.filter(user=current_user)
    Skills=Skills_Model.objects.filter(user=current_user)
    text={
        'edu':edu,
        'exp':exp,
        'Skills':Skills,
    }
 
    return render(req,'profile.html',text)



def updateprofile(req,id):
    data=CreatorProfileModel.objects.filter(id=id)
    dataa=viewersProfileModel.objects.filter(id=id)
    cust=Custom_user.objects.filter(id=id)
    if req.method=='POST':
        id=req.POST.get('id')
        username=req.POST.get("username")
        email=req.POST.get("email")
        user_type=req.POST.get("user_type")
        first_name=req.POST.get("first_name")
        last_name=req.POST.get("last_name")
        Image=req.FILES.get('Image')
        oldimg=req.POST.get('oldimg')

        user_object=Custom_user.objects.get(id=id)

        add=viewersProfileModel(
            id=id,
            user=user_object,
            username=username,
            email=email,
            user_type=user_type,
            first_name=first_name,
            last_name=last_name,
        )
        if Image:
          add.Image=Image
          add.save()
        else:
         add.Image=oldimg
         add.save()
        return redirect ('Profile')
    context={
        'data':data,
        'dataa':dataa,
        'cust':cust,
    }
    return render (req,'updateprofile.html',context)

def addSkill(req):
    current_user=req.user

    skill=intermediate_skillmodel.objects.all()


    if req.method=='POST':
        skill_id=req.POST.get('skill_id')

        skill_object=get_object_or_404(intermediate_skillmodel,id=skill_id)
        if Skills_Model.objects.filter(user=current_user,skill_name=skill_object.skill_name).exists():
            return HttpResponse('skill already exist')
        else:
                    add=Skills_Model(
            user=current_user,
            skill_name=skill_object,
            proficiency_level=req.POST.get('proficiency_level'),

        )
        add.save()
        return redirect ('skill_list')


    return render(req,'addSkill.html',{'skill':skill})


# Edit Skill Function

def editSkill(req,id):
    allskill=Skills_Model.objects.get(id=id)
    skill=intermediate_skillmodel.objects.all()
    
    current_user = req.user
    
    if req.method=='POST':
            Skill_Id = req.POST.get("Skill_Id")
            Skill_Level = req.POST.get("Skill_Level")
            
            MyObj = get_object_or_404(intermediate_skillmodel, id=Skill_Id)
            
            skill = Skills_Model(
                id=id,
                user=current_user,
                skill_name=MyObj.My_Skill_Name,  
                Skill_Level=Skill_Level,
            )
            skill.save()
            return redirect("skill_list")
    
    context={
        "allskill":allskill,
        "skill":skill,
        "proficiency_level":Skills_Model.proficiency_level
    }

    return render(req,'editSkill.html',context)

def skilldeletepage(req,id):
    data=Skills_Model.objects.filter(id=id)
    data.delete()
    return redirect('skill_list')