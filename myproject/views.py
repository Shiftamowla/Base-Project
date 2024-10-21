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


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.warning(request, "Both username and password are required")
            return render(request, "loginPage.html")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully")
            return redirect("base")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def registerpage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        user_type = request.POST.get("usertype")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check for required fields
        if not all([username, email, user_type,password, confirm_password]):
            messages.warning(request, "All fields are required")
            return render(request, "signupPage.html")

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Invalid email format")
            return render(request, "signupPage.html")

        # Check password confirmation
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "signupPage.html")

        # Password validation
        if len(password) < 4:
            messages.warning(request, "Password must be at least 8 characters long")
            return render(request, "signupPage.html")

        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            messages.warning(request, "Password must contain both letters and numbers")
            return render(request, "signupPage.html")

        # Create user
        try:
            user = Custom_user.objects.create_user(
                username=username,
                email=email,
                user_type=user_type,
                password=password,
            )
            if user_type=='viewers':
                viewersProfileModel.objects.create(user=user)
                
            elif user_type=='creator':
                CreatorProfileModel.objects.create(user=user)

            messages.success(request, "Account created successfully! Please log in.")
            return redirect("loginpage")
        except IntegrityError:
            messages.error(request, "Username or email already exists")
            return render(request, "signupPage.html")

    return render(request, "signupPage.html")

def logoutpage(req):
    logout(req)
    return redirect('loginpage')

#profile:


def Profile(req):
    current_user=req.user

    edu=CreatorProfileModel.objects.filter(user=current_user)
    exp=viewersProfileModel.objects.filter(user=current_user)
    text={
        'edu':edu,
        'exp':exp,
    }
 
    return render(req,'profile.html',text)



def updateprofile(req,id):
    data=CreatorProfileModel.objects.filter(id=id)
    dataa=viewersProfileModel.objects.filter(id=id)
    if req.method=='POST':
        id=req.POST.get('id')
        Image=req.FILES.get('Image')
        oldimg=req.POST.get('oldimg')

        user_object=Custom_user.objects.get(id=id)

        add=viewersProfileModel(
            id=id,
            user=user_object,
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
        'dataa':dataa
    }
    return render (req,'updateprofile.html',context)