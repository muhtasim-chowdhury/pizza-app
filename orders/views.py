from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse


from .models import *



# Create your views here.
def index(request):

	# let user register
	if not request.user.is_authenticated:
		return render(request, "orders/register.html", {"message": None})


	

	Small = Size.objects.get(size="Small")
	# if user is logged in, fetch user info and menu
	context = {
		"user": request.user,
		"pizzas": Pizza.objects.filter(size=Small, isMenu=True).all(),
		"toppings": Topping.objects.all()
	}

	# check if user has a cart object
	try:
		shopping_cart = Cart.objects.get(user=request.user)
	except Cart.DoesNotExist:
		# create one
		shopping_cart = Cart(user=request.user)
		shopping_cart.save()


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

	# create a cart for them
	shopping_cart = Cart(user=request.user)
	shopping_cart.save()


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


	Large = Size.objects.get(size="Large")
	if size=="Large":
		p = Pizza.objects.get(pizza=p.pizza, items=p.items, size=Large, isMenu=True)

	
	return HttpResponse(str(p.price))


def addtocart(request):
	# fetch pizza id for pizza that was selected
	pizza_id = request.POST["pizza"]

	# fetch corresponding small pizza
	p = Pizza.objects.get(pk=pizza_id)

	# fetch pizza size
	size = request.POST["size"]


	# if size if large, get corresponding large pizza
	Large = Size.objects.get(size="Large")
	if size=="Large":
		p = Pizza.objects.get(pizza=p.pizza, items=p.items, size=Large, isMenu=True)



	# fetch list of topping ids
	toppings_id = request.POST.getlist('toppings')

	# fetch corresponding toppings
	toppings_array = []
	total = 0
	for idd in toppings_id:
		t = Topping.objects.get(pk=idd)
		toppings_array.append(t)
		total += t.price

	# create requested pizza
	p.pk = None
	p.isMenu = False
	p.user = request.user
	p.price += total
	p.save()


	total = 0
	# iterate through selected toppings and add to new pizza
	for topping in toppings_array:
		p.toppings.add(topping)



	# update shopping cart in database

	shopping_cart = Cart.objects.get(user=request.user)
	shopping_cart.pizzas.add(p)

	# getting current cart total price
	cartTotalPrice = shopping_cart.total

	cartTotalPrice += p.price

	shopping_cart.total = cartTotalPrice
	shopping_cart.save()



	Small = Size.objects.get(size="Small")
	context = {
		"user": request.user,
		"pizzas": Pizza.objects.filter(size=Small, isMenu=True).all(),
		"toppings": Topping.objects.all()
	}





	return render(request, "orders/index.html", context)


def shoppingcart(request):

	# fetch everything in shopping cart
	shopping_cart = Cart.objects.get(user=request.user)

	#get pizzas in cart
	pizzas = shopping_cart.pizzas.all()

	total = shopping_cart.total

	context = {
		"pizzas": pizzas,
		"total": total
	}
	return render(request, "orders/shoppingcart.html", context)



def checkout(request):
	# fetch shopping cart items
	shopping_cart = Cart.objects.get(user=request.user)
	pizzas = shopping_cart.pizzas.all()

	# create Order object
	order = Order(user=request.user)
	order.total = shopping_cart.total
	order.save()

	# add pizzas in cart to order
	for p in pizzas:
		p.id = None
		p.save()
		order.pizzas.add(p)


	# delete cart items
	pizzas.delete()
	shopping_cart.total = 0
	shopping_cart.save()


	return HttpResponseRedirect(reverse('index'))




















































	# # fetch everything in shopping cart
	# shopping_cart = Cart.objects.get(user=request.user)

	# pizzas = shopping_cart.pizzas.all()

	# # add shopping cart items to orders
	# o = Order(user=request.user)
	# o.save()

	# for pizza in pizzas:
	# 	o.pizzas.add(pizza)

	# o.save()
	# # you have to save u dumbass for any change whatsoever






	# # delete items from current user's shopping cart since they have been bought
	# pizzas.delete()


	return HttpResponseRedirect(reverse('index'))