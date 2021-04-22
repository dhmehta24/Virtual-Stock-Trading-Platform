from django.shortcuts import render,redirect
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
        dob = request.POST.get('year') + "-" +  request.POST.get('month')+ "-" + request.POST.get('day')
        gender = request.POST.get('gender')
        psswd = request.POST.get('password')
        cpswd = request.POST.get('cpassword')

        if psswd == cpswd:
            psswd = psswd
        else:
            psswd = None

        '''first_name = ,, , ,, , '''
        user = User.objects.create_user(first_name = full_name.split()[0] , last_name = full_name.split()[1], email = email, password = psswd, username = email.split('@')[0])
        data = Investor(user = user, dob = dob, gender = gender, phone = phone)
        Investor_Staus.objects.create(investor= user)
        data.save()
        #Investor.objects.create(first_name = full_name.split()[0], last_name = full_name.split()[1], email = email, phone = phone, dob = dob, gender = gender, password = psswd, username = email.split('@')[0])

        return render(request,"login-signup.html")
    else:
        pass
    return render(request,"Dashboard.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        psswd = request.POST.get('password')
        remember = request.POST.get('remember-me')

        user = authenticate(username = username, password = psswd)

        if user is not None:
            if remember is not None:
                request.session.set_expiry(settings.KEEP_LOGGED_DURATION)
            login(request, user)
            messages.success(request,"You Have Successfully Logged in :)")
            print("user logged in")
            return redirect("/")

    return redirect('/login')

def logout_user(request):
    logout(request)
    return redirect("/")
