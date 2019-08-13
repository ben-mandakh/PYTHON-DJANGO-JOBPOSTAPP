################### IMPORT SECTION ########################
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .models import Job
import bcrypt

#################### INDEX PAGE ###########################
def index(request):                
    return render(request, "job/index.html")

#################### REGISTRATION #########################

def process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        newUser=User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password = hashed_password)
        newUser.save()
        request.session['id']=newUser.id
        messages.success(request, "User successfully registered")
        return redirect("/success")

#################### SHOW PAGE ############################

def success(request):                
    context = {
        "user": User.objects.get(id = request.session['id']),
        "jobs": Job.objects.all()
        }
    return render(request, "job/show.html", context)

#################### LOGIN ################################

def login(request):
    if (User.objects.filter(email=request.POST['email']).exists()):
        user = User.objects.filter(email=request.POST['email'])[0]
        if (bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())):
            request.session['id'] = user.id
            messages.success(request, "User successfully logged in")
            return redirect('/success')
        messages.success(request, "Password didn't match")
    return redirect('/')

#################### JOB CREATE PAGE ############################

def job(request):                
    return render(request, "job/create.html")

################### ADD JOB FUNCTION #####################

def jobNew(request):
    errors = Job.objects.validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/jobs/new')
    else:
        user = User.objects.get(id = request.session['id'])
        newJob=Job.objects.create(title=request.POST['title'], description=request.POST['desc'], location=request.POST['location'], uploaded_by = user)
        newJob.save()
        user.liked_jobs.add(newJob)
        return redirect("/success")

#################### JOB SHOW ONE FUNCTION #####################

def showOne(request,id):                
    context = {
        "job": Job.objects.get(id=id),
        "jobs": Job.objects.all(),
        "user": User.objects.get(id = request.session['id'])
        }
    return render(request, "job/showOne.html", context)

#################### JOB EDIT PAGE #####################

def update(request,id):                
    context = {
        "job": Job.objects.get(id=id),
        "jobs": Job.objects.all(),
        "user": User.objects.get(id = request.session['id'])
        }
    return render(request, "job/edit.html", context)

################### UPDATE FUNCTION #############################

def edit(request,id):
    errors = Job.objects.validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/jobs/new')
    else:
        u = Job.objects.get(id = id)
        u.title = request.POST['title']
        u.description = request.POST['desc']
        u.location = request.POST['location']
        u.save()
        return redirect ('/success')

#################### DELETE FUNCTION ############################
def delete(request,id):
    d = Job.objects.get(id = id)
    d.delete()
    # d.save()
    return redirect ('/success')

#################### UNFAVORITE FUNCTION ########################
# def unfavorite(request,id):
#     un = Job.objects.get(id = id)
#     un.delete()
#     # d.save()
#     return redirect ('/success')

#################### LOGOUT FUNCTION ############################

def logout(request):
    del request.session['id']
    return redirect('/')































# def show_one(request,id):
#     context = {"show": Show.objects.get(id = id)}
#     return render(request, "show/showOne.html", context)

# def editShow(request, id):                
#     context = {"shows": Show.objects.get(id=id)}
#     return render(request, "show/editShow.html", context)    

# def editShowFunction(request,id):
#     errors = Show.objects.basic_validator(request.POST)
#     if len(errors) > 0:
#         for key, value in errors.items():
#             messages.error(request, value)
#         return redirect(f'/shows/{id}/edit')
#     else:
#         u = Show.objects.get(id = id)
#         u.title=request.POST['title']
#         u.network=request.POST['network']
#         u.release_date=request.POST['release_date']
#         u.desc = request.POST['desc']
#         u.save()
#         messages.success(request, "Blog successfully updated")
#         return redirect ("/shows")

# def delete(request,id):
#     d = Show.objects.get(id = id)
#     d.delete()
#     return redirect ("/shows")


