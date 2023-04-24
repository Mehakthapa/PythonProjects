from django.shortcuts import redirect, render
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate , login , logout
# Create your views here.

# def home(request):
#     return HttpResponse("welcome to your app home")

def home(request):
    return render(request, "authentication/index.html")


def register(request):
    if request.method =="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpass = request.POST['cpassword']
        # username = request.POST.get('')


        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('register')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('register')
        

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('register')
        
       
        if password != confirmpass:
            messages.error(request,"Password didn't matched ")
            return redirect('register')
        
        
   

        # register user in backend
        myusers = User.objects.create_user(username,email,password)



        myusers.user_name = username
        myusers.email = email
        myusers.save()

        messages.success(request, 'Your account has been successfully registered ')

        return redirect('signin')


    return render(request, "authentication/register.html")



def signin(request):

    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
     

        user = authenticate(username = username , password=password)


        if user is not None:
            login(request, user)
            user_name = user.username
            return render(request, "authentication/index.html", {'user_name' : user_name})
        
        else:
            messages.error(request,'Wrong credentials')

            return redirect('home')

    return render(request, "authentication/login.html")



def signout(request):
    logout(request)
    messages.success(request, "You are successfully logout")
    return redirect('home')