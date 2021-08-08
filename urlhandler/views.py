from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required   #this is for redirect user to login page if it not logged in
from django.contrib import messages
from .models import shorturl
import random
import string

# Create your views here.
def home(request,query=None):   #query if someone append any string than first find it in database
    if not query or query is None:
        return render(request, 'home.html')
    else:
        try:
            check = shorturl.objects.get(short_query=query)
            check.save()
            url_to_redirect = check.original_url 
            return redirect(url_to_redirect)
        except shorturl.DoesNotExist:
            return render(request, 'home.html', {'error': "error"})

def contact(request):
    return render(request,'contact.html')

@login_required(login_url='/login')
def dash(request):
    usr=request.user
    urls=shorturl.objects.filter(user=usr)
    return render(request,'dashboard.html',{'urls':urls})

def randomgen():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

def price(request):
    return render(request,'price.html')

@login_required(login_url='/login/')
def generate(request):
    if request.method == "POST":
        if request.POST['original'] and request.POST['short']:
            usr=request.user
            original=request.POST['original']
            short=request.POST['short']
            check=shorturl.objects.filter(short_query=short)
            if not check:
                newurl=shorturl(
                    user=usr,
                    short_query=short,
                    original_url=original
                )
                newurl.save()
                return redirect(dash)
            else:
                messages.error(request,"Already Exists")
                return redirect(dash)
        elif request.POST['original']:
            # generate randomly
            usr = request.user
            original = request.POST['original']
            generated = False
            while not generated:
                short = randomgen()
                check = shorturl.objects.filter(short_query=short)
                if not check:
                    newurl = shorturl(
                        user=usr,
                        original_url=original,
                        short_query=short,
                    )
                    newurl.save()
                    return redirect(dash)
                else:
                    continue
        else:
            messages.error(request, "Empty Fields")
            return redirect(dash)
    else:
        return redirect('/dash')