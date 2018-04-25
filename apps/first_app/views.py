from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.

def index(request):
	
	return render(request,"login_reg.html")

def validate(request):
	# if request.method == "POST":
	errors = Guest.objects.reg_validator(request.POST)
	if len(errors):
		request.session['name'] =request.POST['name']
		request.session['username'] =request.POST['reg_username']
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		guest = Guest.objects.create()
		guest.name = request.POST['name']
		guest.username = request.POST['reg_username']
		guest.password =  bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())		

		guest.save()
		request.session['id'] = guest.id

		messages.success(request, "successfully registered! ")
       	
	return redirect('/dashboard')


def login(request):
	errors = Guest.objects.log_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		guest = Guest.objects.get(username = request.POST['log_username'])
		request.session['name'] = guest.name
		request.session['id'] = guest.id

		messages.success(request, "successfully registered! ")
		return redirect('/dashboard')



def dashboard(request):
	user = Guest.objects.get(id = request.session['id'])
	context = {"items" : Item.objects.exclude(wisher=user),
				"my_items" : Item.objects.filter(wisher=user),
				"self_item" : Item.objects.filter(created_by=user)}		
	return render(request, "dashboard.html", context)


def process(request):
	return render(request, 'addItem.html')


def create(request):
	if request.method == "POST":
		item = Item.objects.create(
			name = request.POST['item_name'],
			created_by = Guest.objects.get(id= request.session['id'])
			)
		return redirect('/dashboard')

		
		
	return redirect("/process")

def addItem(request, id):
	# if request.method == "POST":
		# this user veriable becomes the login user
	user = Guest.objects.get(id= request.session['id'])
		# greb the item id
	item = Item.objects.get(id= id)
	user.wish.add(item)
	return redirect('/dashboard')

def removeItem(request,id):
	user = Guest.objects.get(id= request.session['id'])
	item = Item.objects.get(id=id)
	item.wisher.remove(user)
	return redirect('/dashboard')



def delete(request, id):
	deleteuser =Item.objects.get(id=id)
	deleteuser.delete()
	return redirect('/dashboard')



def show(request, id):
	show = Item.objects.get(id=id)
	user = {
		"name" : show.name,
		"username" : show.wisher.all()
		}
	return render(request, "show.html", user)

def logout(request):
	request.session.clear()
	return redirect('/')