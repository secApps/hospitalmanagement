from django.shortcuts import render, redirect
from django.db import connection


def login_view(request):
    user = None
    if request.method == "POST":
        print("clicked")
        name = request.POST.get("user")
        passw = request.POST.get("password")
        # query = "SELECT * FROM user WHERE email = %s and password = %s"
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE email = %s and password = %s", [name, passw])
            user = dictfetchall(cursor)
            if len(user) > 0:
                return redirect('/user_list/')

    return render(request, "login.html", {
        'user': user

    })


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def user_list_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user")
        users = dictfetchall(cursor)
    return render(request, "user_list.html", {
         'users': users

    })
