from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import re
import bcrypt

# Create your views here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
def index(request):
	# User.userManager.login("speros@codingdojo.com", "Speros") 
	return render(request,"login_app/index.html")


def register(request):
	if request.method == 'POST':
		x = False
		if not EMAIL_REGEX.match(request.POST['email']):
			messages.info(request, ' Invalid email ')
			x = True
			# return redirect('/')
		if not NAME_REGEX.match(request.POST['name']):
			messages.info(request, ' Invalid name ')
			x = True
			# return redirect('/')
		if not NAME_REGEX.match(request.POST['alias']):
			messages.info(request, ' Invalid alias ')
			x = True
			# return redirect('/')
		if len(request.POST['password']) < 8:
			messages.info(request,'Password must be atleast 8 characters long')
			x = True
			# return redirect('/')
		elif request.POST['password'] != request.POST['confirm_password']:
			messages.info(request,'Password and confirm password are not matched')
			x = True
			# return redirect('/')

		if x:
			return redirect('/')

		else:
			password = request.POST['password'].encode()
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			user = User.userManager.create(name=request.POST['name'],alias=request.POST['alias'],email = request.POST['email'],password=hashed,date=request.POST['date'] )

	print ('**************')
	try:
		request.session['name'] = request.POST['name']
		request.session['user_id'] = user.id
	except:
		request.session['name'] = ""
		request.session['user_id'] = 0
	return redirect('/success')

def success(request):

	if request.session['name'] == "":
		return redirect('/')
	else:
		logged_in_user = User.userManager.get(id=request.session['user_id'])
		people_poked_you = logged_in_user.poke.all
		
		count = len(User.objects.get(id=request.session['user_id']).poke.all())
		user = User.objects.filter(id=request.session['user_id'])
		for user in user:
			users = User.objects.all().exclude(id=user.id)
			



		context = {
		'users':users,
		'people_poked_you':people_poked_you,
		'count' : count
		}

		return render(request,"login_app/success.html",context)

def logout(request):
	request.session['name'] = ""
	request.session['user_id'] = 0
	return redirect('/')

def add_poke(request,id):

	poke_to = User.userManager.get(id=id)
	poke_by = User.userManager.get(id=request.session['user_id'])
	poke_to.poke.add(poke_by)
	poke_to.save
	poke_by.poke_to.add(poke_to)
	poke_by.save

	print("*******")
	print('poke_to')
	print(poke_to.name)
	print('poke_by')
	print(poke_by.name)

	# print(poke_by.poke.all())
	# print(poke_to.poke.all())
	pokers = poke_by.poke_to.all()
	poke_too = poke_to.poke.all()

	for poker in pokers:
		print poker.name
		print('000000')

	count = 0
	for poker in poke_too:
		print poker.name
		print('ppppppp')
		count = count+1
		print(count)

	
	return redirect('/success')

def login(request):
	
	email = request.POST['email']
	password = request.POST['password']
	x = False;

	if len(email) == 0:
		messages.error(request, "email is required")
		x = True;

	elif not User.userManager.filter(email = email).exists():
		messages.error(request, "email is not in the database")
		x=True;

	if x:
		return redirect('/')
	else:
		password = password.encode()
		user = User.userManager.get(email = email)
		ps_hashed = user.password
		ps_hashed = ps_hashed.encode()
		request.session['name'] = user.name
		request.session['user_id'] = user.id
		if bcrypt.hashpw(password, ps_hashed) == ps_hashed:
			request.session['user_id'] = user.id
			request.session['name'] = user.name
			return redirect('/success')
		else:
			messages.error(request, "email or password does not match")
			return redirect('/')




























