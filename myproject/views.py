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

def appliedJob(request):
    current_user = request.user

    # Get all job applications for the current user
    job_applications = ApplyJobModel.objects.filter(user=current_user)

    job_messages = {}
    for job_application in job_applications:
        messages = ApplyJobModel.objects.filter(application=job_application)
        job_messages[job_application.id] = messages

    context = {
        "Job": job_applications,
        "job_messages": job_messages, 
    }
    return render(request, "applyedJob.html", context)

def ApplyNow(req,job_title,apply_id):
    
    current_user=req.user
    
    if current_user.user_type == 'jobseeker':
        
        specific_job=JobModel.objects.get(id=apply_id)
        
        already_exists=ApplyJobModel.objects.filter(user=current_user,job=specific_job).exists()
        
        context={
            'specific_job':specific_job,
            'already_exists':already_exists
        }   
        if req.method=='POST':
            Full_Name=req.POST.get("Full_Name")
            Work_Experience=req.POST.get("Work_Experience")
            Skills=req.POST.get("Skills")
            Linkedin_URL=req.POST.get("Linkedin_URL")
            Expected_Salary=req.POST.get("Expected_Salary")
            Resume=req.FILES.get("Resume")
            Cover=req.POST.get("Cover")
            
            apply=ApplyJobModel(
                user=current_user,
                job=specific_job,
                Resume=Resume,
                Full_Name=Full_Name,
                Work_Experience=Work_Experience,
                Skills=Skills,
                Expected_Salary=Expected_Salary,
                Linkedin_URL=Linkedin_URL,
                Cover=Cover,
                status="pending"
            )
            apply.save()
            return redirect("jobfeed")
            
        return render(req,"applyjob.html",context)
    else:
        messages.warning(req,"You are not a Job Seeker")

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
    current_user=req.user
    
    if req.method=='POST':
        username=req.POST.get("username")
        email=req.POST.get("email")
        first_name=req.POST.get("first_name")
        last_name=req.POST.get("last_name")
        company_logo_old=req.POST.get("company_logo_old")
        Image=req.FILES.get("Image")
        
        
        current_user.username=username
        current_user.email=email
        current_user.first_name=first_name
        current_user.last_name=last_name
        
        
        try:
            creatorProfile=CreatorProfileModel.objects.get(user=current_user)
            if Image:
                creatorProfile.Image=Image
                creatorProfile.save()
                current_user.save()

            else:
                creatorProfile.Image=company_logo_old
                creatorProfile.save()
                current_user.save()
            
            return redirect("Profile")
            
        except CreatorProfileModel.DoesNotExist:
            creatorProfile=None
            
        try:
            viewersProfile=viewersProfileModel.objects.get(user=current_user)

            if Image:
                viewersProfile.Image=Image
                viewersProfile.save()
                current_user.save()

            else:
                viewersProfile.Image=company_logo_old
                viewersProfile.save()
                current_user.save()

            
            return redirect("Profile")
            
        except viewersProfileModel.DoesNotExist:
            viewersProfile=None

    return render (req,'updateprofile.html')

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