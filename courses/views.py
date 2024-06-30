from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout

def logout_user(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        if key == 'session_key':
            continue
        del request.session[key]
    logout(request)
    return render(request, 'registration/logged_out.html')
