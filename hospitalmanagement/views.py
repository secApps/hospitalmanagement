from django.shortcuts import render
from django.db import connection


def login_view(request):
    return render(request, "login.html", {

    })
