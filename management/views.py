from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from .models import User

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    if request.method == 'POST':
        photo = None
        if (request.FILES):
            photo = request.FILES["profile_image"]
        email = request.POST["email"]
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]

        user = User.objects.get(username=request.user.username)

        if photo is not None and user is not None:
            user.first_name = firstName
            user.last_name = lastName
            user.email = email
            user.photo = photo
            user.save()
        elif photo is None and user is not None:
            user.first_name = firstName
            user.last_name = lastName
            user.email = email
            user.save()
        
        user = User.objects.get(username=request.user.username)
        return render(request, 'management/index.html', {
            'details' : user,
            'message' : 'Success'
        })

    
    user = User.objects.get(username=request.user.username)
    return render(request, 'management/index.html', {
        'details' : user,
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'management/login.html', {
                "message": "invalid username or password" 
            })

    return render(request, 'management/login.html')

def register(request):
    if request.method == "POST":
        photo = request.FILES["profile_image"]
        username = request.POST["username"]
        password = request.POST["password"]
        cpassword = request.POST["confirmation"]

        if password != cpassword:
            return render(request, 'management/register.html', {
                "message": "Passwords don't match!" 
            })
        elif not password or not username or not photo:
            return render(request, 'management/register.html', {
                "message": "Missing Content!" 
            })
        
        try:
            user = User.objects.create_user(username=username, password=password, photo=photo)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, 'management/register.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))