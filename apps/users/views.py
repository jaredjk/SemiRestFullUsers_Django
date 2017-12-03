from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
# Create your views here.
def index(request):
    response = 'Semi-Restful Users'
    return HttpResponse(response)

def users(request):
    return render(request, 'users/userdash.html', {'all_users':User.objects.all()}) #'all_users' with ORM Commands User.objects.all()
    #goes to userdash.html to show all users.

# def show(request, user_number):
#     response = 'connected to show', user_number
#     return render(request, '/users/show', {'user':User.objects.get(id=user_number)})

def new(request): #user/new directs to users/usercreate.html
    return render(request, 'users/usercreate.html') 

def create(request): 
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST) #function from models.py / validator
        if len(errors) > 0: #if there is error.
            for error in errors.itervalues(): #for error in errors(functions in models.py)
                messages.error(request, error) #return message from functions in models.py and send message to usercreate.HTML
            return redirect('/users/new') 
        else:
            User.objects.create(name=request.POST['inputted_name'], email=request.POST['inputted_email'])
            return redirect('/users') #inputted_name from html to ORM command. 

def edit(request, user_number):
    return render(request, 'users/userupdate.html', {'user':User.objects.get(id=user_number)})

def update(request, user_number):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0: 
            for error in errors.itervalues():
                messages.error(request, error)
            temp_url = '/users/edit' + user_number #get info on user 
            return redirect(temp_url)
        else:
            temp = User.objects.get(id=user_number) 
            if request.POST['inputted_name']:
                temp.name = request.POST['inputted_name']
            if request.POST['inputted_email']:
                temp.email = request.POST['inputted_email']
            temp.save()
            temp_url = '/users/' + user_number
    return redirect(temp_url)

def delete(request, user_number):
    User.objects.get(id=user_number).delete() 
    return redirect('/users')