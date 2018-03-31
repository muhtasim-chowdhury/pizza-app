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


class Pizza(models.Model):
	pizza = models.ForeignKey(Style, on_delete=models.CASCADE, related_name="style")
	items = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item")
	sprice = models.DecimalField(max_digits=4, decimal_places=2)
	lprice = models.DecimalField(max_digits=4, decimal_places=2)

	def __str__(self):
		return f"{self.pizza} {self.items}"

class Topping(models.Model):
	name = models.CharField(max_length=15)
	pizzas = models.ManyToManyField(Pizza, blank=True, related_name="toppings")

	def __str__(self):
		return self.name

class Order(models.Model):
	# order items
	user = models.CharField(max_length=20)
	name = models.CharField(max_length=15)
	details = models.CharField(max_length=40, blank=True)
	price = models.DecimalField(max_digits=4, decimal_places=2)
	
	def __str__(self):
		return f"{self.name} {self.details} {self.price}"



class Cart(models.Model):
	# cart items
	user = models.CharField(max_length=20, blank=True)
	name = models.CharField(max_length=15)
	details = models.CharField(max_length=40, blank=True)
	price = models.DecimalField(max_digits=4, decimal_places=2)
	

	def __str__(self):
		return f"{self.name} {self.details} {self.price}"



