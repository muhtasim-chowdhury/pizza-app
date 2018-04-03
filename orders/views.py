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
		"toppings": Topping.objects.all(),
		"subs": Sub.objects.filter(isMenu=True).all(),
		"pastas": Pasta.objects.filter(isMenu=True).all(),
		"salads": Salad.objects.filter(isMenu=True).all(),
		"platters": Dinner_Platter.objects.filter(isMenu=True).all()
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
	if pizza_id != '0':
		size = request.POST['size']
		p = Pizza.objects.get(pk=pizza_id)


		# fetch list of topping ids
		toppings_id = request.POST['toppings'].split(",")
		
		total = 0

		if toppings_id[0] != '':
			print(len(toppings_id))
			# fetch corresponding toppings
			for idd in toppings_id:
				t = Topping.objects.get(pk=int(idd))
				total += t.price

		Large = Size.objects.get(size="Large")
		if size=="Large":
			p = Pizza.objects.get(pizza=p.pizza, items=p.items, size=Large, isMenu=True)

		pizza_price = p.price
	else:
		pizza_price = 0
		total = 0
	# fetch sub price if selected
	sub_id = request.POST['subs']
	if sub_id != '0':
		s = Sub.objects.get(pk=int(sub_id))
		sp = s.price
	else:
		sp = 0



	pasta_id = request.POST['pastas']
	if pasta_id != '0':
		pa = Pasta.objects.get(pk=int(pasta_id))
		pasta_price  = pa.price
	else:
		pasta_price = 0


	salad_id = request.POST['salads']
	if salad_id != '0':
		sa = Salad.objects.get(pk=int(salad_id))
		salad_price  = sa.price
	else:
		salad_price = 0



	platter_id = request.POST['platters']
	if platter_id != '0':
		dp = Dinner_Platter.objects.get(pk=int(platter_id))
		platter_price  = dp.price
	else:
		platter_price = 0







	price = pizza_price + total + sp + pasta_price + salad_price + platter_price

	
	return HttpResponse(str(price))


def addtocart(request):
	# get shoppings cart
	shopping_cart = Cart.objects.get(user=request.user)



	# fetch pizza id for pizza that was selected
	pizza_id = request.POST["pizza"]
	if pizza_id is not '0':
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

		# make a copy
		p.pk = None
		p.isMenu = False
		p.user = request.user
		p.price += total
		p.save()
		
		for topping in toppings_array:
			p.toppings.add(topping)
		shopping_cart.pizzas.add(p)

		pizza_price = p.price
	else:
		pizza_price = 0
	


	sub_id = request.POST['sub']
	sub_price = 0
	if sub_id is not '0':
		sub = Sub.objects.get(pk=sub_id)
		sub.id = None
		sub.isMenu = False
		sub.user = request.user
		sub.save()
		shopping_cart.subs.add(sub)
		sub_price = sub.price


	pasta_id = request.POST['pasta']
	pasta_price = 0
	if pasta_id is not '0':
		pasta = Pasta.objects.get(pk=pasta_id)
		pasta.id = None
		pasta.isMenu = False
		pasta.user = request.user
		pasta.save()
		shopping_cart.pastas.add(pasta)
		pasta_price = pasta.price

	salad_id = request.POST['salad']
	salad_price = 0
	if salad_id is not '0':
		salad = Salad.objects.get(pk=salad_id)
		salad.id = None
		salad.isMenu = False
		salad.user = request.user
		salad.save()
		shopping_cart.salads.add(salad)
		salad_price = salad.price


	platter_id = request.POST['platter']
	platter_price = 0
	if platter_id is not '0':
		platter = Dinner_Platter.objects.get(pk=platter_id)
		platter.id = None
		platter.isMenu = False
		platter.user = request.user
		platter.save()
		shopping_cart.platters.add(platter)
		platter_price = platter.price



	# getting current cart total price
	cartTotalPrice = shopping_cart.total

	cartTotalPrice += pizza_price + sub_price + pasta_price + salad_price + platter_price

	shopping_cart.total = cartTotalPrice
	shopping_cart.save()



	# Small = Size.objects.get(size="Small")
	# context = {
	# 	"user": request.user,
	# 	"pizzas": Pizza.objects.filter(size=Small, isMenu=True).all(),
	# 	"toppings": Topping.objects.all(),
	# 	"subs": Sub.objects.filter(isMenu=True).all(),
	# 	"pastas": Pasta.objects.filter(isMenu=True).all(),
	# 	"salads": Salad.objects.filter(isMenu=True).all(),
	# 	"platters": Dinner_Platter.objects.filter(isMenu=True).all()
	# }





	# return render(request, "orders/index.html", context)
	return HttpResponseRedirect(reverse('index'))

def shoppingcart(request):

	# fetch everything in shopping cart
	shopping_cart = Cart.objects.get(user=request.user)

	#get pizzas in cart
	pizzas = shopping_cart.pizzas.all()
	subs = shopping_cart.subs.all()
	pastas = shopping_cart.pastas.all()
	salads = shopping_cart.salads.all()
	platters = shopping_cart.platters.all()


	total = shopping_cart.total


	


	context = {
		"pizzas": pizzas,
		"total": total,
		"subs": subs,
		"pastas": pastas,
		"salads": salads,
		"platters": platters
	}
	return render(request, "orders/shoppingcart.html", context)



def checkout(request):
	# fetch shopping cart items
	shopping_cart = Cart.objects.get(user=request.user)
	pizzas = shopping_cart.pizzas.all()
	subs = shopping_cart.subs.all()
	pastas = shopping_cart.pastas.all()
	salads = shopping_cart.salads.all()
	platters = shopping_cart.platters.all()

	# create Order object
	order = Order(user=request.user)
	order.total = shopping_cart.total
	order.save()

	# add pizzas in cart to order
	for p in pizzas:
		p.id = None
		p.save()
		order.pizzas.add(p)

	for s in subs:
		s.id = None
		s.save()
		order.subs.add(s)

	for pa in pastas:
		pa.id = None
		pa.save()
		order.pastas.add(pa)

	for sa in salads:
		sa.id = None
		sa.save()
		order.salads.add(sa)

	for pl in platters:
		pl.id = None
		pl.save()
		order.platters.add(pl)

	# delete cart items
	pizzas.delete()
	subs.delete()
	pastas.delete()
	salads.delete()
	platters.delete()
	shopping_cart.total = 0
	shopping_cart.save()

	return HttpResponseRedirect(reverse('index'))

def clear(request):
	shopping_cart = Cart.objects.get(user=request.user)
	shopping_cart.pizzas.all().delete()
	shopping_cart.subs.all().delete()
	shopping_cart.pastas.all().delete()
	shopping_cart.salads.all().delete()
	shopping_cart.platters.all().delete()
	shopping_cart.total = 0
	shopping_cart.save()
	return render(request, "orders/shoppingcart.html")













# for administrative use
def clean(request):
	pizzas = Pizza.objects.filter(isMenu=False).all()
	pizzas.delete()
	subs = Sub.objects.filter(isMenu=False).all()
	subs.delete()
	pastas = Pasta.objects.filter(isMenu=False).all()
	pastas.delete()
	salads = Salad.objects.filter(isMenu=False).all()
	salads.delete()
	platters = Dinner_Platter.objects.filter(isMenu=False).all()
	platters.delete()

	shopping_cart = Cart.objects.get(user=request.user)
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