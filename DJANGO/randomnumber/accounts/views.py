from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from ratelimit.decorators import  ratelimit
from ratelimit.core import get_usage, is_ratelimited
from django.http import HttpResponse

# Create your views here.
@ratelimit(key='post:username', rate='5/m', method=['POST'],block=True)
def call_api(request):
    if request.user.is_authenticated:
        return redirect('http://127.0.0.1:5000/home')
    else:
        return redirect('login')

    
def see_remaining_limits(request):
    usage=get_usage(request, fn=call_api, key='post:username', rate='5/m', method=['POST'])
    count=usage['count']
    res=300-count
    if res<0:
        res=0
    return HttpResponse(res)

def home(request):
    return render(request,'home.html')

def login(request):
    if request.method=='POST':
        username=request.POST["username"]
        password=request.POST["password"]   
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return render(request,'login.html')
    else:
        return render(request,'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
def resister(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST["username"]
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2 :
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('resister')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('resister')

            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                messages.info(request,'user created')
                return redirect('login')
        else:
            messages.info(request,'password not matching')
            return redirect('resister')

        return redirect('/')
    else:
        return render(request,'resister.html')