from django.shortcuts import render,redirect
from django.contrib.auth.models import User #django built in user model
from django.contrib import messages,auth    #auth is authentication model in django

# Create your views here.
def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            try:
                user=User.objects.get(email=request.POST['email'],password=request.POST['password'])
                auth.login(request,user)
                return render(request,'home.html')  #if user deatils are match
            except User.DoesNotExist:
                print("execption")
                return render(request,'login.html',{'error':"User Doesn't Exist"})  #if user is not registered
        else:
            return render(request,'login.html')  #if it is not a post request
    else:
        return redirect('/')
    
def signup(request):
    if request.method == "POST":
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.get(email=request.POST['email'])
                if user:
                    return render(request, 'login.html', {'error': "User Already Exists"})
            except User.DoesNotExist:
                User.objects.create(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password1'],
                )
                messages.success(request, "Signup Successfull! Now Login Here")
                return redirect(login)
        else:
            messages.error(request, "Enter Same Passwords!!!")
            return render(request,'signup.html')
    else:
        return render(request,'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('/login')