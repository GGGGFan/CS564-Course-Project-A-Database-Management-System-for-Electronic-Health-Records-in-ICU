from django.shortcuts import render
from django.db import connection
from django.contrib import messages
from django.http import HttpResponseRedirect
import sys
sys.path.append('../query')
from query.models import Stay, Patients

# This is the basic delete function to guide the page to delete.html
def delete(request):
    return render(request, 'delete/delete.html')

# This is the function for deleting all the stay belongs to a specific patient
def delete_pt(request):
    ptid = request.GET['ptid']
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM stay WHERE uniquepid = %s", [ptid])

    messages.success(request, 'Delete Successfully!')
    next = request.META.get('HTTP_REFERER', '/')

    return HttpResponseRedirect(next)

# This is the function to search the stayID belongs to a pateient
def delete_stay(request):
    ptid = request.GET['ptid']
    with connection.cursor() as cursor:
        cursor.execute("SELECT patientunitstayid FROM stay WHERE uniquepid=  %s", [request.GET['ptid']])
        allStays = cursor.fetchall()
    return render(request, 'delete/delete_stay.html', {'allStays':[i[0] for i in allStays], 'ptid':ptid})

# This is the function to perfrom the stay deletion based on the provided stayID.
def delete_success(request):
    ptid = request.GET['ptid']
    stayid = request.GET['stayid']
    if stayid == 'All':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM stay WHERE uniquepid = %s", [ptid])
    else:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM stay WHERE patientunitstayid = %s", [stayid])

    messages.success(request, 'Delete Successfully!')
    next = request.META.get('HTTP_REFERER', '/')

    return HttpResponseRedirect(next)
