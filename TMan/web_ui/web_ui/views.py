from django.shortcuts import redirect

def login_redirect(reqest):
    return redirect('/task/login')

def home(request):
    return redirect('/task/home')