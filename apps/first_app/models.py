from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class userManager(models.Manager):
	def reg_validator(self, postData):
		errors ={}
		serverUsername = Guest.objects.filter(username = postData['reg_username'])
		if len(postData['name']) < 4:
			errors['name'] = "Name should be at least 4 characters"

		# elif len(postData['last_name']) < 2:
		# 	errors['last_name'] = "Last Name should be at least 2 characters"

		elif len(postData['reg_username']) < 1:
			errors['username'] = "please enter username"

		elif postData['password'] != postData['con_pass']:
			errors['con_pass'] = "Please confirm your password"

		elif len(postData['password']) < 8:
			errors['pw'] = "please enter more than 8 characters for your password"

		# elif not EMAIL_REGEX.match(postData['reg_email']):
		# 	errors['reg_email'] = "Please enter a valid email"

		elif len(serverUsername):
			errors['serverUsername'] = "username has already existed!"

		return errors 


	def log_validator(self, postData):
		errors = {}
		checkUser = Guest.objects.filter(username=postData['log_username'])
		checkPw = Guest.objects.filter(password = postData['log_password'])

		if len(postData['log_username']) < 1:
			errors['username'] = "please enter your username"
		if len(checkUser) == 0:
			errors['match'] = "invalid username and password" 
		return errors

class Guest(models.Model):
	item = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now_add = True)
	objects = userManager()

class Item(models.Model):
	name = models.CharField(max_length=255)
	created_by = models.ForeignKey(Guest, related_name = "created_by")
	wisher = models.ManyToManyField(Guest, related_name = "wish")
	created_at = models.DateTimeField(auto_now_add = True)
	objects = userManager()