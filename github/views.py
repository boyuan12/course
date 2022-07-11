from django.shortcuts import redirect, render
from helpers import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, GITHUB_REDIRECT_URI
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def github_authorize(request):
    return redirect(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}")

def github_callback(request):
    code = request.GET["code"]
    data = requests.post("https://github.com/login/oauth/access_token", data={
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": request.GET["code"]
    }, headers={
        "Accept": "application/json"
    })

    request.session["github_access_token"] = data.json()["access_token"]

    r = requests.get("https://api.github.com/user", headers={
        "Authorization": f"token {request.session['github_access_token']}"
    })
    gh_username = r.json()["login"]
    gh_email = r.json()["email"]

    user = authenticate(username=gh_username, password="github")
    if user is not None:
        login(request, user)
    else:
        user = User.objects.create_user(username=gh_username, email=gh_email, password="github")
        login(request, user)
    
    return redirect("/")
