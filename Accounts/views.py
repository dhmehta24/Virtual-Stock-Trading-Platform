from django.shortcuts import render,redirect, reverse
from .models import User,Investor
from Portfolio.models import Investor_Staus
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.contrib import messages
# Create your views here.

def register(request):
    return render(request,"login-signup.html")

def register_user(request):
    if request.method == "POST":
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('date')
        gender = request.POST.get('gender')
        psswd = request.POST.get('password')
        cpswd = request.POST.get('cpassword')

        if psswd == cpswd:
            psswd = psswd
        else:
            messages.error(request, "Passwords Didn't Match")
            return redirect("user_login")

        '''first_name = ,, , ,, , '''
        user = User.objects.create_user(email = email, password = psswd, username = email)
        data = Investor(user = user, dob = dob, gender = gender, phone = phone, investor_name=full_name)
        Investor_Staus.objects.create(investor= user)
        try:
            data.save()
        except IntegrityError:
            messages.error(request,"User with same email already exist !")
            return redirect("user_login")
        print("User Created")
        messages.success(request,"Register Succeed, Your username is {}".format(email))
        #Investor.objects.create(first_name = full_name.split()[0], last_name = full_name.split()[1], email = email, phone = phone, dob = dob, gender = gender, password = psswd, username = email.split('@')[0])

        return render(request,"login-signup.html")
    else:
        pass
    return render(request,"Dashboard.html")

def login_user(request):
    if request.method == "POST":
        email = request.POST.get('username')
        psswd = request.POST.get('password')
        remember = request.POST.get('remember-me')

        user = authenticate(username = email, password = psswd)

        if user is not None:
            if remember is not None:
                request.session.set_expiry(settings.KEEP_LOGGED_DURATION)
            login(request, user=user)
            messages.success(request,"You Have Successfully Logged in :)")
            print("User logged in")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('user_login')

def update_profile(request):
    if request.method == "POST":
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')

        user = Investor.objects.get(user=request.user)
        user.user.username = email
        user.phone = phone
        user.dob = dob
        user.investor_name = full_name
        user.save()

        messages.success(request,"Profile Updated Successfully !")

        return redirect('user_profile')


def logout_user(request):
    logout(request)
    messages.success(request,"You Have Successfully Logged Out")
    return redirect("/")
