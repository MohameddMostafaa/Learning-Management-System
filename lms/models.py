import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password


class AccountTypes(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.name}" 


class RegisteredGroups(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.name}" 



class User(AbstractUser):
    name = models.CharField(max_length=200)
    group = models.ForeignKey(RegisteredGroups, on_delete=models.CASCADE)
    type = models.ForeignKey(AccountTypes, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.password[:13] == "pbkdf2_sha256":
            super().save(*args, **kwargs)
        else:
            self.password = make_password(self.password)
            super().save(*args, **kwargs)



class PendingAccounts(models.Model):
    name = models.CharField(max_length=200) 
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    emailVerified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.password[:13] == "pbkdf2_sha256":
            super().save(*args, **kwargs)
        else:
            self.password = make_password(self.password)
            super().save(*args, **kwargs)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)



class Courses(models.Model):
    name = models.CharField(max_length=300)
    code = models.CharField(max_length=10, unique=True)
    group = models.ForeignKey(RegisteredGroups, on_delete=models.CASCADE)



class Posts(models.Model):
    yes_no_choices = (
        ('on', 'on'),
        ('off', 'off'),
    )
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000, null=True)
    canSubmit = models.CharField(max_length=3, choices=yes_no_choices, default='Off')
    file = models.FileField(upload_to='documents/%Y/%m/%d', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)



class Submissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    text = models.CharField(max_length=5000, null=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d', null=True)

    def filename(self):
        return os.path.basename(self.file.name)
