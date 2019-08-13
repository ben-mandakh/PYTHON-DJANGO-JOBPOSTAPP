############## IMPORT SECTION ######################################

from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

############## MANAGER FOR USER TABLE ##############################

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors["fname"] = "First name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "Last name should be at least 2 characters"
        if len(postData['email']) < 1:
            errors["email"] = "Email should be at least 1 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["emailP"] = "Invalid email address!"
        this_email = User.objects.filter(email=postData['email'])
        if len(this_email)>0:
            errors['email'] = "User already exists!"
        print("Inside account ")
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 3 characters"
        if postData['cpassword'] != postData['password']:
            errors["cpassword"] = "Password must match"
        return errors

############## MANAGER FOR JOB TABLE ###############################

class JobManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors["title"] = "Title should be at least 3 characters"
        if len(postData['desc']) < 3:
            errors["desc"] = "Desciption should be at least 3 characters"
        if len(postData['location']) < 3:
            errors["location"] = "Location should be at least 3 characters"
        return errors

############## USER MODEL ###########################################

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

############## JOB MODEL ###########################################

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="jobs")          # ONE TO MANY RELATIONS HERE
    users_who_like = models.ManyToManyField(User, related_name="liked_jobs")     # MANY TO MANY RELATIONS HERE
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()