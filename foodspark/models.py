from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
import hashlib
from django.core.validators import  *
from django.core.exceptions import ValidationError
import datetime


# Create your models here.
class Restaurant(models.Model):
	email = models.EmailField(primary_key = True)
	password = models.CharField(max_length=100)
	name = models.CharField(max_length=200)
	address = models.TextField()
	RES_TYPE = (   ############fill it up##################################################@#
		('B','Bar'),
		('R','Restaurant'),
		('C','Cafe')
	)
	res_type = models.CharField(max_length=1,choices = RES_TYPE,default = 'R')
	cuisine = models.CharField(null = True, max_length=100)
	# RATING = (
	# 	('1','1'),
	# 	('2','2'),
	# 	('3','3'),
	# 	('4','4'),
	# 	('5','5')
	# )
	#rating = models.CharField(null = True,max_length=1,choices = RATING) 
	city = models.CharField(max_length = 100,null = True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") #############look into regex
	phone = models.CharField(validators=[phone_regex],max_length=15,blank = True) 
	image = models.ImageField(default = '/home/projjal/Projects/Foodspark/foodspark/static/img') ############################################################
	def make_password(self ,password):
		assert password
		hashedpassword = hashlib.md5(password).hexdigest()
		return hashedpassword
	def check_password(self, password):
		assert password
		hashed = hashlib.md5(password).hexdigest()
		return self.password == hashed
	def set_password(self, password):
		self.password = password

class Customer(models.Model):
	# userid = models.CharField(primary_key = True,max_length =50)
	password = models.CharField(max_length=100)
	name = models.CharField(max_length=200)
	address = models.TextField()
	city = models.CharField(max_length = 100)
	email = models.EmailField(primary_key = True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.") #############look into regex
	phone = models.CharField(validators=[phone_regex],max_length=15,blank = True)
	def make_password(self ,password):
		assert password
		hashedpassword = hashlib.md5(password).hexdigest()
		return hashedpassword
	def check_password(self, password):
		assert password
		hashed = hashlib.md5(password).hexdigest()
		return self.password == hashed
	def set_password(self, password):
		self.password = password

	def details(self):
		return {
			'userid' : self.userid,
			'name' : self.name,
			'email' : self.email,
			'password' : self.password,
			'phone' : self.phone
		}

#class Admin(models.Model):   #######################
#	adminid = models.ForeignKey(Customer,on_delete=models.CASCADE,primary_key=True)

class FoodItem(models.Model):
	resid = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	cuisine = models.CharField(max_length=100)
	COURSE = (
		('s','Starter'),
		('m','Main Course'),
		('d','Desert')
	)
	course = models.CharField(max_length=1,choices=COURSE)
	price = models.IntegerField()
	availability_time = models.TimeField()
	image = models.ImageField() ###########################################################
	# group = models.ForeignKey()

# class Payment(models.Model):
# 	amount = models.IntegerField()
# 	discount = models.IntegerField()

class Order(models.Model):
 	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
 	restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
 	foodlist = models.CharField(max_length = 500,validators=[validate_comma_separated_integer_list],null=True)
 	amount = models.IntegerField(default = 0)
	ordertime = models.TimeField(default= datetime.datetime.now())
	DSTATUS = (
		('p','Pending'),
		('d','Delivered')
	)
	deliverystatus = models.CharField(max_length=1,choices=DSTATUS,default = 'p')
	PSTATUS = (
		('P','Paid'),
		('N','Not Paid')
	)
	paymentstatus = models.CharField(max_length=1,choices=PSTATUS,default = 'N')


	def calamount(self):
		self.amount = 0
		myl = self.foodlist.split(",")
		for x in myl:
			fitem = FoodItem.objects.get(pk=int(x))
			self.amount = self.amount + fitem.price



	
