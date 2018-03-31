from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse

#import models
from .models import *



# Create your views here.
def index(request):

	# let user register
	if not request.user.is_authenticated:
		return render(request, "orders/register.html", {"message": None})
	
	# if user is logged in, fetch user info and menu
	context = {
		"user": request.user,
		"pizzas": Pizza.objects.all()
	}


	# fetch shopping cart
	shopping_cart = Cart.objects.all()


	try:
		context["cart"] = shopping_cart
	except KeyError:
		context["cart"] = None

	return render(request, "orders/index.html", context)



# STRICTLY FOR POST REQUEST
def register(request):
	user = request.POST["user"]
	password = request.POST["pass"]
	u = authenticate(request, username=user, password=password)
	if u:
		# user already has an account
		return render(request, "orders/register.html", {"message": "That username already exists"})

	# otherwise create account for new user
	u = User.objects.create_user(username=user, password=password)
	u.save()
	login(request, u)
	return HttpResponseRedirect(reverse('index'))

def login_view(request):
	user = request.POST["user"]
	password = request.POST["pass"]
	u = authenticate(request, username=user, password=password)
	
	# invalid account
	if u is None:
		return render(request, "orders/register.html", {"message": "Username and/or Password is incorrect"})

	# otherwise log them in
	login(request, u)

	return HttpResponseRedirect(reverse('index'))

def logout_view(request):
	logout(request)
	# return HttpResponseRedirect(reverse('index'))
	return render(request, "orders/register.html", {"message": "You have logged out"})

def ajax(request):
	# fetch form data
	pizza_id = request.POST['type']
	size = request.POST['size']
	p = Pizza.objects.get(pk=pizza_id)
	

	if size == 'small':
		price = p.sprice
	else:
		price = p.lprice
	return HttpResponse(str(price))
	# return JsonResponse({ "price": str(price)})

def addtocart(request):
	pizza_id = request.POST["pizza"]
	p = Pizza.objects.get(pk=pizza_id)
	size = request.POST["size"]

	if size == 'small':
		price = p.sprice
	else:
		price = p.lprice



	# update shopping cart in database
	current = Cart(user=request.user, name=p, details=size.capitalize(), price=price)
	current.save()

	context = {
		"user": request.user,
		"pizzas": Pizza.objects.all(),
	}

	return render(request, "orders/index.html", context)


def shoppingcart(request):

	# fetch everything in shopping cart
	shopping_cart = Cart.objects.filter(user=request.user).all()

	total = 0
	for item in shopping_cart:
		total += item.price


	context = {
		"cart": shopping_cart,
		"total": total
	}
	return render(request, "orders/shoppingcart.html", context)



def checkout(request):

	# fetch everything in shopping cart
	shopping_cart = Cart.objects.filter(user=request.user).all()



	# add shopping cart items to orders
	for item in shopping_cart:
		current = Order(user=request.user, name=item.name, details=item.details, price=item.price)
		current.save()


	# delete items from current user's shopping cart since they have been bought
	Cart.objects.filter(user=request.user).delete()


	return HttpResponseRedirect(reverse('index'))