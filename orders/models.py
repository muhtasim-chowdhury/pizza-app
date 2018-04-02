from django.db import models

# Create your models here.
class Style(models.Model):
	name = models.CharField(max_length=10)

	def __str__(self):
		return self.name

class Item(models.Model):
	name = models.CharField(max_length=15)

	def __str__(self):
		return self.name


class Size(models.Model):
	size = models.CharField(max_length=5)
	def __str__(self):
		return self.size


class Topping(models.Model):
	name = models.CharField(max_length=16)
	

	def __str__(self):
		return self.name


class Pizza(models.Model):
	isMenu = models.BooleanField(default=True)
	user = models.CharField(max_length=15, blank=True)
	pizza = models.ForeignKey(Style, on_delete=models.CASCADE, related_name="pizza")
	items = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="pizza")
	size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="pizza")
	price = models.DecimalField(max_digits=4, decimal_places=2)
	toppings = models.ManyToManyField(Topping, blank=True)

	def topping_set(self):
		return self.toppings.all()
	

	def __str__(self):
		return f"{self.size} {self.pizza} {self.items} Menu: {self.isMenu}"


class Cart(models.Model):
	user = models.CharField(max_length=15, blank=True)
	pizzas = models.ManyToManyField(Pizza, blank=True)
	total = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)

	def __str__(self):
		return self.user +"'s Cart"

class Order(models.Model):
	user = models.CharField(max_length=15, blank=True)
	pizzas = models.ManyToManyField(Pizza, blank=True)
	total = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)

	def __str__(self):
		return self.user +"'s Order"











# class Cart(models.Model):
# 	# cart items
# 	user = models.CharField(max_length=20, blank=True)
# 	name = models.CharField(max_length=15)
# 	details = models.CharField(max_length=40, blank=True)
# 	price = models.DecimalField(max_digits=4, decimal_places=2)
	

# 	def __str__(self):
# 		return f"{self.name} {self.details} {self.price}"




# class Order(models.Model):
# 	# order items
# 	user = models.CharField(max_length=20)
# 	name = models.CharField(max_length=15)
# 	details = models.CharField(max_length=40, blank=True)
# 	price = models.DecimalField(max_digits=4, decimal_places=2)
	
# 	def __str__(self):
# 		return f"{self.name} {self.details} {self.price}"