from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.urls import reverse_lazy



from .forms import RegisterForm, LogInForm

def registration_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("goodfood:main")
    else:
        form = RegisterForm()

    
    return render(request, "registration.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        form = LogInForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("goodfood:main")
    else:
        form = LogInForm()        
    return render(request, "login.html", {"form": form})
        
            
            
                
    
  