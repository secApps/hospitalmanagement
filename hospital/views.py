import sys

from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from rest_framework.decorators import api_view


@api_view(['POST'])
def login_view(request):
    user = None
    if request.method == "POST":
        email = request.data['user']
        passw = request.data['password']
        print("ep:", email, passw, request.data, "oioi")
        query = "SELECT user.id,user.email, user_role.role_id FROM user,user_role WHERE user.id = user_role.user_id " \
                "and user.email = %s and user.password = %s "
        with connection.cursor() as cursor:
            cursor.execute(query, [email, passw])
            user = dictfetchall(cursor)
            print(user)
            if len(user) > 0:
                return JsonResponse({
                    'status': "true",
                    'data': user[0]})

    return JsonResponse({
        'status': "false",
        'data': None})


@api_view(['POST'])
def update_user(request):
    user = None
    if request.method == "POST":
        email = request.data['email']
        passw = request.data['password']
        name = request.data['name']
        mobile = request.data['mobile']
        role = request.data['role']
        query = "INSERT INTO user ( email, password, user_name, mobile) VALUES(%s,%s,%s,%s)"
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [email, passw, name, mobile])
                if cursor.rowcount > 0:
                    user_id = cursor.lastrowid
                    query = "INSERT INTO user_role ( user_id, role_id) VALUES(%s,%s)"
                    cursor.execute(query, [user_id, role])
                    if cursor.rowcount > 0:
                        return JsonResponse({
                            'status': "true",
                            'id': user_id})
        except:
            return JsonResponse({
                'status': "false"})

    return JsonResponse({
        'status': "false"})


@api_view(['POST'])
def update_prescription(request):
    if request.method == "POST":
        patient_id = request.data['patient_id']
        doctor_id = request.data['doctor_id']
        advice = request.data['advice']
        medicine = request.data['medicine']
        diagnosis = request.data['diagnosis']
        notes = request.data['notes']
        query = "INSERT INTO prescription ( patient_id, doctor_id, advice, notes) VALUES(%s,%s,%s,%s)"
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [patient_id, doctor_id, advice, notes])
                if cursor.rowcount > 0:
                    prescription_id = cursor.lastrowid
                    query1 = "INSERT INTO prescription_diagnosis (prescription_id, diagnosis_id) VALUES(%s,%s)"
                    query2 = "INSERT INTO prescription_medicine ( prescription_id, medicine_id) VALUES(%s,%s)"
                    cursor.execute(query1, [prescription_id, diagnosis])
                    cursor.execute(query2, [prescription_id, medicine])
                    if cursor.rowcount > 0:
                        return JsonResponse({
                            'status': "true"})
        except:
            print(sys.exc_info())
            return JsonResponse({
                'status': "false"})

    return JsonResponse({
        'status': "false"})


@api_view(['POST'])
def add_people(request):
    user = None
    if request.method == "POST":
        user_id = request.data['user_id']
        ssn = request.data['ssn']
        f_name = request.data['f_name']
        l_name = request.data['l_name']
        address = request.data['address']
        who = request.data['who']
        if who == "Patient":
            query = "INSERT INTO patient ( user_id, ssn, first_name, last_name, address) VALUES(%s,%s,%s,%s,%s)"
        elif who == "Doctor":
            query = "INSERT INTO doctor ( user_id, ssn, first_name, last_name, address,speciality) VALUES(%s,%s,%s,%s,%s,%s)"
        elif who == "Diagnostician":
            query = "INSERT INTO diagnostician ( user_id, ssn, first_name, last_name, address, lab_name) VALUES(%s,%s,%s,%s,%s,%s)"
        else:
            query = "INSERT INTO receptionist ( user_id, ssn, first_name, last_name, address) VALUES(%s,%s,%s,%s,%s)"
        try:
            with connection.cursor() as cursor:
                if who == "Patient":
                    cursor.execute(query, [user_id, ssn, f_name, l_name, address])
                elif who == "Doctor":
                    speciality = request.data['speciality']
                    cursor.execute(query, [user_id, ssn, f_name, l_name, address, speciality])
                elif who == "Diagnostician":
                    lab_name = request.data['lab_name']
                    cursor.execute(query, [user_id, ssn, f_name, l_name, address, lab_name])
                else:
                    cursor.execute(query, [user_id, ssn, f_name, l_name, address])

                if cursor.rowcount > 0:
                    return JsonResponse({
                        'status': "true",
                        'id': cursor.lastrowid})
        except Exception as i:
            print(i)
            return JsonResponse({
                'status': "false"
            })

    return JsonResponse({
        'status': "false"})


@api_view(['POST'])
def update_appointments(request):
    user = None
    if request.method == "POST":
        patient_id = request.data['patient_id']
        doctor_id = request.data['doctor_id']
        when = request.data['date']

        query = "INSERT INTO appoinments ( patient_id, doctor_id, app_date) VALUES(%s,%s,%s)"
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [patient_id, doctor_id, when])
                if cursor.rowcount > 0:
                    return JsonResponse({
                        'status': "true"})
        except:
            return JsonResponse({
                'status': "false"})

    return JsonResponse({
        'status': "false"})


@api_view(['POST'])
def user_list_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user")
        users = dictfetchall(cursor)
    return render(request, "user_list.html", {
        'users': users

    })


@api_view(['POST'])
def todo_diagnosis_report_for_diagnostician(request):
    diagnostician = request.data['diag_id']
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM doctor,prescription,prescription_diagnosis,diagnosis, diagnostician where doctor.id = "
            "prescription.doctor_id and prescription.id = prescription_diagnosis.prescription_id and diagnosis.id = "
            "prescription_diagnosis.diagnosis_id and diagnosis.diagnostician_id = diagnostician.id and "
            "diagnostician.id = %s and is_delivered > 0", [diagnostician])
        reports = dictfetchall(cursor)
    return JsonResponse({
        'reports': reports})


@api_view(['POST'])
def user_list(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM user,role,user_role where user.id = user_role.user_id and role.id = user_role.role_id")
        users = dictfetchall(cursor)
    return JsonResponse({
        'users': users})


@api_view(['POST'])
def patient_list(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM patient,user where  patient.user_id = user.id")
        users = dictfetchall(cursor)
    return JsonResponse({
        'users': users})


@api_view(['POST'])
def appointment_list(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM patient,appoinments,doctor where  patient.id = appoinments.patient_id and doctor.id = "
            "appoinments.doctor_id and appoinments.app_date > now() order by appoinments.app_date desc")
        appointments = dictfetchall(cursor)
    return JsonResponse({
        'appointments': appointments})


@api_view(['POST'])
def doctor_appointment_list(request):
    doc_id = request.data['doc_id']
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM patient,appoinments,doctor where  patient.id = appoinments.patient_id and doctor.id = "
            "appoinments.doctor_id and appoinments.app_date > now() and doctor.id= %s order by appoinments.app_date "
            "desc",
            [doc_id])
        users = dictfetchall(cursor)
    return JsonResponse({
        'users': users})


@api_view(['POST'])
def medicine_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM medicine")
        medicine = dictfetchall(cursor)
    return JsonResponse({
        'medicines': medicine})


@api_view(['POST'])
def diagnosis_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM diagnosis")
        diagnosis = dictfetchall(cursor)
    return JsonResponse({
        'diagnosis': diagnosis})


@api_view(['POST'])
def doctor_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM doctor")
        doctor = dictfetchall(cursor)
    return JsonResponse({
        'doctor': doctor})


@api_view(['POST'])
def role_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM role")
        roles = dictfetchall(cursor)
    return JsonResponse({
        'role': roles})


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def create_user_view(request):
    return render(request, "read_user.html", None)


def update_user_view(request):
    return render(request, "read_user.html", None)


def read_user_view(request):
    return render(request, "read_user.html", None)


def delete_user_view(request):
    return render(request, "read_user.html", None)
