from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from churan_s4.sql_database import *
import re

def index(request):
    return render(request, 'churan_s4/index.html')

def advancequery(request):
    if request.method == "POST":
        if 'semester' in request.POST:
            semester = request.POST.get('semester')
            try:
                attribute_1, attribute_2 = semester.lstrip().split(' ', 1)
                attribute_1 = attribute_1.strip()
                attribute_2 = attribute_2.strip()
            except:
                context = {"error_msg": "Input Format Error."}
                return render(request, 'churan_s4/error.html', context)
            year = 0
            season = ''
            if attribute_1.isnumeric() and not attribute_2.isnumeric():
                year = eval(attribute_1)
                season = attribute_2.lower()
            elif attribute_2.isnumeric() and not attribute_1.isnumeric():
                year = eval(attribute_2)
                season = attribute_1.lower()
            else:
                context = {"error_msg": "Input Format Error."}
                return render(request, 'churan_s4/error.html', context)
            result = stage_3_advquery(year, season)
            context = {'year':year, 'season':season, 'rows': result}
            return render(request, 'churan_s4/advancequery.html', context)
        else:
            return HttpResponseRedirect('/churan')
    else:
        return HttpResponseRedirect('/churan')

def create(request):
    if request.method == "POST":
        if ('email' in request.POST) and ('username' in request.POST) and ('password' in request.POST):
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
            if not (re.search(regex, email)):
                context = {"error_msg": "Invalid email format."}
                return render(request, 'churan_s4/error.html', context)
            if len(password) < 8:
                context = {"error_msg": "Password too short."}
                return render(request, 'churan_s4/error.html', context)
            result = create_user(email, username, password)
            if result == 0:
                msg = "User \"" + username + "\" is successfully created."
                context = {"suc_msg":  msg}
                return render(request, 'churan_s4/success.html', context)
            else:
                if result == 1062:
                    context = {"error_msg": "Username has been used."}
                    return render(request, 'churan_s4/error.html', context)
                else:
                    context = {"error_msg": "Something is wrong."}
                    return render(request, 'churan_s4/error.html', context)
        else:
            return HttpResponseRedirect('/churan')
    else:
        return HttpResponseRedirect('/churan')

def update(request):
    if request.method == "POST":
        if ('username' in request.POST) and ('oldpassword' in request.POST) and ('newpassword' in request.POST):
            username = request.POST.get('username')
            oldpassword = request.POST.get('oldpassword')
            newpassword = request.POST.get('newpassword')
            if len(newpassword) < 8:
                context = {"error_msg": "New password too short."}
                return render(request, 'churan_s4/error.html', context)
            result = check_user(username, oldpassword)
            if result:
                update_user(username, newpassword)
                msg = "User \"" + username + "\" password is successfully updated."
                context = {"suc_msg":  msg}
                return render(request, 'churan_s4/success.html', context)
            else:
                context = {"error_msg": "Wrong Username or Old Password."}
                return render(request, 'churan_s4/error.html', context)
        else:
            return HttpResponseRedirect('/churan')
    else:
        return HttpResponseRedirect('/churan')

def delete(request):
    if request.method == "POST":
        if ('username' in request.POST) and ('password' in request.POST):
            username = request.POST.get('username')
            password = request.POST.get('password')
            result = check_user(username, password)
            if result:
                remove_user(username, password)
                msg = "User \"" + username + "\" is no longer in the database."
                context = {"suc_msg":  msg}
                return render(request, 'churan_s4/success.html', context)
            else:
                context = {"error_msg": "Wrong Username or Password."}
                return render(request, 'churan_s4/error.html', context)
        else:
            return HttpResponseRedirect('/churan')
    else:
        return HttpResponseRedirect('/churan')

def showalluser(request):
    result = show_all_user()
    context = {"rows": result}
    return render(request, 'churan_s4/showalluser.html', context)

def addcourse(request):
    if request.method == "POST":
        if ('course_number' in request.POST) and ('course_name' in request.POST) and ('dept_name' in request.POST) and ('course_GPA' in request.POST) and ('credits' in request.POST):
            course_number = request.POST.get('course_number').upper()
            course_name = request.POST.get('course_name')
            dept_name = request.POST.get('dept_name').upper()
            course_GPA = request.POST.get('course_GPA')
            credits = request.POST.get('credits')
            try:
                course_number.index(dept_name)
            except:
                context = {"error_msg": "Wrong Course Number or Department."}
                return render(request, 'churan_s4/error.html', context)
            if not (course_GPA.replace('.','',1).isdigit() or credits.isdigit()):
                context = {"error_msg": "Wrong GPA or Credit."}
                return render(request, 'churan_s4/error.html', context)
            if eval(course_GPA) < 0 or eval(course_GPA) > 4 or eval(credits) < 0 or eval(credits) > 4:
                context = {"error_msg": "Wrong GPA or Credit."}
                return render(request, 'churan_s4/error.html', context)
            result = create_course(course_number, course_name, dept_name, course_GPA, credits)
            if result == 0:
                msg = "Course \"" + course_number + "\" is successfully created."
                context = {"suc_msg":  msg}
                return render(request, 'churan_s4/success.html', context)
            else:
                if result == 1062:
                    context = {"error_msg": "Course is already in database."}
                    return render(request, 'churan_s4/error.html', context)
                elif result == 1452:
                    context = {"error_msg": "Wrong Department."}
                    return render(request, 'churan_s4/error.html', context)
                else:
                    context = {"error_msg": "Something is wrong."}
                    return render(request, 'churan_s4/error.html', context)
        else:
            return HttpResponseRedirect('/churan')
    else:
        return HttpResponseRedirect('/churan')
    return None

def findcourse(request):
    if request.method == "POST":
        if ('course_number' in request.POST):
            course_number = request.POST.get('course_number').upper()
            if course_number.isalpha():
                result = find_course_by_dept(course_number)    
                context = {"course_number": course_number, "rows": result}
                return render(request, 'churan_s4/courseinfo.html', context)
            else:
                result = find_course_by_cn(course_number)    
                context = {"course_number": course_number, "rows": result}
                return render(request, 'churan_s4/courseinfo.html', context)
        else:
            return HttpResponseRedirect('/churan')
    else:
        return HttpResponseRedirect('/churan')

def updatecourse(request):
    if request.method == "POST":
        if ('course_number' in request.POST) and ('course_GPA' in request.POST) and ('credits' in request.POST):
            course_number = request.POST.get('course_number').upper()
            course_GPA = request.POST.get('course_GPA')
            credits = request.POST.get('credits')
            if not (course_GPA.replace('.','',1).isdigit() or credits.isdigit()):
                context = {"error_msg": "Wrong GPA or Credit."}
                return render(request, 'churan_s4/error.html', context)
            if eval(course_GPA) < 0 or eval(course_GPA) > 4 or eval(credits) < 0 or eval(credits) > 4:
                context = {"error_msg": "Wrong GPA or Credit."}
                return render(request, 'churan_s4/error.html', context)
            result = check_course(course_number)
            if result:
                update_course(course_number, course_GPA, credits)
                msg = "Course \"" + course_number + "\" information is successfully updated."
                context = {"suc_msg":  msg}
                return render(request, 'churan_s4/success.html', context)
            else:
                context = {"error_msg": "Course is not in database."}
                return render(request, 'churan_s4/error.html', context)
        else:
            return HttpResponseRedirect('/churan')
    else:
        return HttpResponseRedirect('/churan')

def deletecourse(request):
    if request.method == "POST":
        if ('course_number' in request.POST):
            course_number = request.POST.get('course_number').upper()
            result = check_course(course_number)
            if result:
                remove_course(course_number)
                msg = "Course \"" + course_number + "\" is no longer in the database."
                context = {"suc_msg":  msg}
                return render(request, 'churan_s4/success.html', context)
            else:
                context = {"error_msg": "Course is not in database."}
                return render(request, 'churan_s4/error.html', context)
        else:
            return HttpResponseRedirect('/churan')
    else:
        return HttpResponseRedirect('/churan')
