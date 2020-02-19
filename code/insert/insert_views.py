import random
from django.shortcuts import render
from django.db import connection
from django.contrib import messages
from django.http import HttpResponseRedirect
import json
import sys
sys.path.append('../query')
from query.models import Stay, Patients

# This the function django use to guide the page to insert.html
def insert(request):
    return render(request, 'insert/insert.html')

# This is the functon to generate a new patient
def new_patient(request):
    # Generate a new id
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT uniquepid FROM patients WHERE uniquepid LIKE '%999-'")
        ptids = cursor.fetchall()
    # because uniquepid is in the format of 123-12345
    ptids = [i[4:] for i in ptids]
    new_ptid = str(random.randint(10000,99999))
    while new_ptid in ptids:
        new_ptid = random.randint(10000,99999)
    new_ptid = '999-' + new_ptid # we assign new id to 999- area

    new_patient = Patients.objects.create(uniquepid=new_ptid)

    messages.success(request, 'Patient ' + str(new_ptid) + ' has been added!')
    next = request.META.get('HTTP_REFERER', '/')

    return HttpResponseRedirect(next)

# This is the function to generate a new stay for the specific patient
def new_stay(request):
    ptid = request.GET['ptid']
    try:
        pt_obj = Patients.objects.get(uniquepid=ptid)
    except:
        messages.success(request, 'Please offer a valid uniquepid')
        next = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(next)

    # Retrive existing data
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM stay WHERE uniquepid=  %s", [ptid])
        stay = cursor.fetchone()

    new_age = request.GET['new_age']
    # if an attribute is leaving blank, display the previously recored data
    if not new_age and stay:
        new_age = stay[2]

    new_admisionweight = request.GET['new_admisionweight']
    if not new_admisionweight and stay:
        new_admisionweight = stay[6]

    new_admisionheight = request.GET['new_admisionheight']
    if not new_admisionheight and stay:
        new_admisionheight = stay[4]

    new_unittype = request.GET['new_unittype']
    if not new_unittype and stay:
        new_unittype = stay[5]

    new_dischargestatus = request.GET['new_dischargestatus']
    if not new_dischargestatus and stay:
        new_dischargestatus = stay[8]

    new_gender = request.GET['new_gender']
    if not new_gender and stay:
        new_gender = stay[1]

    new_ethnicity = request.GET['new_ethnicity']
    if not new_ethnicity and stay:
        new_ethnicity = stay[3]

    # Create new stay

    # Generate a new id
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT patientunitstayid FROM stay WHERE patientunitstayid IS NOT NULL")
        ptids = cursor.fetchall()
    ptids = [i[0] for i in ptids]
    new_stayid = random.randint(100000,999999)
    while new_stayid in ptids:
        new_stayid = random.randint(100000,999999)
    del ptids

    new_stay = Stay.objects.create(patientunitstayid=new_stayid, uniquepid=ptid, gender=new_gender, age=new_age, ethnicity=new_ethnicity, admissionweight=new_admisionweight,
                                    admissionheight=new_admisionheight, unittype=new_unittype, unitdischargestatus=new_dischargestatus)

    return render(request, 'insert/new_stay.html', {'stayid': new_stayid,
                                                    'ptid': ptid,
                                                    'new_age': new_age,
                                                    'new_gender': new_gender,
                                                    'new_ethnicity': new_ethnicity,
                                                    'new_admisionweight':new_admisionweight,
                                                    'new_admisionheight': new_admisionheight,
                                                    'new_unittype': new_unittype,
                                                    'new_dischargestatus': new_dischargestatus})

# This is the function for search the data filed id, like labid, medicationid and etc. under a specific stay.
def modify_data(request):
    stayid = request.GET['stayid']
    datafield = request.GET['datafield']
    try:
        Stay_obj = Stay.objects.get(patientunitstayid=stayid)
    except:
        messages.success(request, 'Please provide valid stayid!')
        next = request.META.get('HTTP_REFERER', '/')

        return HttpResponseRedirect(next)

    # Get the ID List
    datafield = request.GET['datafield']
    if datafield == 'diagnosis':
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT diagnosisid FROM diagnosis WHERE diagnosisid IS NOT NULL AND patientunitstayid = %s", (stayid,))
            dgids = cursor.fetchall()
    elif datafield == 'lab':
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT labid FROM lab WHERE labid IS NOT NULL AND patientunitstayid = %s", (stayid,))
            dgids = cursor.fetchall()
    elif datafield == 'microlab':
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT microlabid FROM microlab WHERE microlabid IS NOT NULL AND patientunitstayid = %s", (stayid,))
            dgids = cursor.fetchall()
    elif datafield == 'medication':
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT medicationid FROM medication WHERE medicationid IS NOT NULL AND patientunitstayid = %s", (stayid,))
            dgids = cursor.fetchall()
    elif datafield == 'allergy':
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT allergyid FROM allergy WHERE allergyid IS NOT NULL AND patientunitstayid = %s", (stayid,))
            dgids = cursor.fetchall()
    else:
        pass

    print(dgids)
    listA = []
    for i in dgids:
        listA.append(i[0])
    print(listA)

    typelist = json.dumps(listA)
    print(typelist)

    return render(request, 'insert/new_modified_id_selection.html', {'typeid': typelist, 'stayid':stayid, 'datafield': datafield})

# This is the function to find the data under the specific data field ID.
def modify_data_select(request):
    datafield = request.GET['datafield']
    idname = request.GET['typeID']

    if datafield == "diagnosis":
        idtype = "diagnosisid"
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM diagnosis WHERE diagnosisid = %s", (idname,))
            dic = dictfetchall(cursor)
    elif datafield == "lab":
        idtype = "labid"
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM lab WHERE labid = %s", (idname,))
            dic = dictfetchall(cursor)
    elif datafield == "microlab":
        idtype = "microlabid"
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM microlab WHERE microlabid = %s", (idname,))
            dic = dictfetchall(cursor)
    elif datafield == "medication":
        idtype = "medicationid"
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM medication WHERE medicationid = %s", (idname,))
            dic = dictfetchall(cursor)
    elif datafield == "allergy":
        idtype = "allergyid"
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM allergy WHERE allergyid = %s", (idname,))
            dic = dictfetchall(cursor)

    return render(request, 'insert/new_modified_data.html', {'datafield': datafield, 'typeID': idname, 'dictAttri': json.dumps(dic[0])})

# This the function to modify the data based on provided data.
def modify_data_modified(request):

    datafield = request.GET['datafield']
    typeID = request.GET['typeID']
    print(datafield)
    print(typeID)

    if request.GET['datafield'] == 'diagnosis':
        icd9code = request.GET['icd9code']
        diagnosisoffset = request.GET['diagnosisoffset']
        print("icd9code is: " + str(icd9code))
        print(diagnosisoffset)
        # Update
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE diagnosis SET
                 icd9code = %s,
                 diagnosisOffset = %s
                 WHERE diagnosisid = %s;
            """,(icd9code, diagnosisoffset,typeID,))
    elif request.GET['datafield'] == 'lab':
        labType = request.GET['labType']
        labName = request.GET['labName']
        labResult = request.GET['labResult']
        labMeasureNameSystem = request.GET['labMeasureNameSystem']
        labResultOffset = request.GET['labResultOffset']
        # Update
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE lab SET
                 labresultoffset = %s,
                 labtypeid = %s,
                 labname = %s,
                 labresult = %s,
                 labmeasurenamesystem = %s
                WHERE
                 labid = %s;
            """, (labResultOffset, labType, labName, labResult, labMeasureNameSystem, typeID, ))
    elif request.GET['datafield'] == 'microlab':
        organism = request.GET['organism']
        cultureSite = request.GET['cultureSite']
        sensitivityLevel = request.GET['sensitivityLevel']
        antibiotic = request.GET['antibiotic']
        cultureTakenOffset = request.GET['cultureTakenOffset']
        # Insert
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE microlab SET
                 organism = %s,
                 cultureSite = %s,
                 sensitivityLevel = %s,
                 antibiotic = %s,
                 cultureTakenOffset = %s
                WHERE
                 microlabid = %s
            """, (organism, cultureSite, sensitivityLevel, antibiotic, cultureTakenOffset,typeID, ))
    elif request.GET['datafield'] == 'medication':
        routeAdmin = request.GET['routeAdmin']
        drugName = request.GET['drugName']
        dosage = request.GET['dosage']
        drugoffset = request.GET['drugOffset']
        # Insert
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE medication SET
                 routeAdmin = %s,
                 drugName = %s,
                 dosage = %s,
                 drugoffset = %s
                WHERE
                 medicationid = %s
            """, (routeAdmin, drugName, dosage, drugoffset,typeID,))
    elif request.GET['datafield'] == 'allergy':
        allergyName = request.GET['allergyName']
        allergyType = int(request.GET['allergyType'])
        allergyOffset = int(request.GET['allergyOffset'])
        # Insert
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE allergy SET
                 allergyname = %s,
                 allergytype = %s,
                 allergyoffset = %s
                WHERE
                 allergyid = %s
            """, (allergyName, allergyType, allergyOffset,typeID,))
    else:
        pass

    messages.success(request, 'Record has been modified!')
    next = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(next)

# This is the function for guide the page to new_data.html page with stayid and datafield.
def new_data(request):
    stayid = request.GET['stayid']
    try:
        Stay_obj = Stay.objects.get(patientunitstayid=stayid)
    except:
        return render(request, 'insert/insert.html', {'no_stay':1})
    datafield = request.GET['datafield']
    return render(request, 'insert/new_data.html', {'datafield':datafield, 'stayid':stayid})

# This is the function for add new data.
def data_added(request):
    stayid = request.GET['stayid']

    if request.GET['datafield'] == 'diagnosis':
        icd9code = request.GET['icd9code']
        diagnosisoffset = request.GET['diagnosisoffset']
        # Generate a new id
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT diagnosisid FROM diagnosis WHERE diagnosisid IS NOT NULL")
            dgids = cursor.fetchall()
        dgids = [i[0] for i in dgids]
        new_dgid = random.randint(100000,999999)
        while new_dgid in dgids:
            new_dgid = random.randint(1000000,9999999)
        del dgids
        # Insert
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO diagnosis (
                 diagnosisid,
                 patientunitstayid,
                 icd9code,
                 diagnosisOffset)
                VALUES
                 (%s,%s,%s,%s)
            """,(new_dgid, stayid, icd9code, diagnosisoffset,))
    elif request.GET['datafield'] == 'lab':
        labType = request.GET['labType']
        labName = request.GET['labName']
        labResult = request.GET['labResult']
        labMeasureNameSystem = request.GET['labMeasureNameSystem']
        labResultOffset = request.GET['labResultOffset']
        # Generate a new id
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT labid FROM lab WHERE labid IS NOT NULL")
            dgids = cursor.fetchall()
        dgids = [i[0] for i in dgids]
        new_dgid = random.randint(100000,999999)
        while new_dgid in dgids:
            new_dgid = random.randint(1000000,9999999)
        del dgids
        # Insert
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO lab (
                 labid,
                 patientunitstayid,
                 labresultoffset,
                 labtypeid,
                 labname,
                 labresult,
                 labmeasurenamesystem)
                VALUES
                 (%s,%s,%s,%s,%s,%s,%s)
            """, (new_dgid, stayid, labResultOffset, labType, labName, labResult, labMeasureNameSystem,))
    elif request.GET['datafield'] == 'microlab':
        organism = request.GET['organism']
        cultureSite = request.GET['cultureSite']
        sensitivityLevel = request.GET['sensitivityLevel']
        antibiotic = request.GET['antibiotic']
        cultureTakenOffset = request.GET['cultureTakenOffset']
        # Generate a new id
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT microlabid FROM microlab WHERE microlabid IS NOT NULL")
            dgids = cursor.fetchall()
        dgids = [i[0] for i in dgids]
        new_dgid = random.randint(100000,999999)
        while new_dgid in dgids:
            new_dgid = random.randint(1000000,9999999)
        del dgids
        # Insert
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO microlab (
                 microlabid,
                 patientunitstayid,
                 organism,
                 cultureSite,
                 sensitivityLevel,
                 antibiotic,
                 cultureTakenOffset
                 )
                VALUES
                 (%s,%s,%s,%s,%s,%s,%s)
            """, (new_dgid, stayid, organism, cultureSite, sensitivityLevel, antibiotic, cultureTakenOffset,))
    elif request.GET['datafield'] == 'medication':
        routeAdmin = request.GET['routeAdmin']
        drugName = request.GET['drugName']
        dosage = request.GET['dosage']
        drugoffset = request.GET['drugOffset']
        # Generate a new id
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT medicationid FROM medication WHERE medicationid IS NOT NULL")
            dgids = cursor.fetchall()
        dgids = [i[0] for i in dgids]
        new_dgid = random.randint(100000,999999)
        while new_dgid in dgids:
            new_dgid = random.randint(1000000,9999999)
        del dgids
        # Insert
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO medication (
                 medicationid,
                 patientunitstayid,
                 routeAdmin,
                 drugName,
                 dosage,
                 drugoffset
                 )
                VALUES
                 (%s,%s,%s,%s,%s,%s)
            """, (new_dgid, stayid, routeAdmin, drugName, dosage, drugoffset,))
    elif request.GET['datafield'] == 'allergy':
        allergyName = request.GET['allergyName']
        allergyType = int(request.GET['allergyType'])
        allergyOffset = int(request.GET['allergyOffset'])
        # Generate a new id
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT allergyid FROM allergy WHERE allergyid IS NOT NULL")
            dgids = cursor.fetchall()
        dgids = [i[0] for i in dgids]
        new_dgid = random.randint(100000,999999)
        while new_dgid in dgids:
            new_dgid = random.randint(1000000,9999999)
        del dgids
        # Insert
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO allergy
                (
                 allergyid,
                 patientunitstayid,
                 allergyname,
                 allergytype,
                 allergyoffset
                 )
                VALUES
                 (%s,%s,%s,%s,%s);
            """, (new_dgid, stayid, allergyName, allergyType, allergyOffset,))

    else:
        pass

    messages.success(request, 'New Record has been added!')
    next = request.META.get('HTTP_REFERER', '/')

    return HttpResponseRedirect(next)

# Function for selecting dictionary from SQL
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
