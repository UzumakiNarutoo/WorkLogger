from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import Sum
from django.db.models.deletion import SET_NULL


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("Users must have a username.")
        if not email:
            raise ValueError("Users must have an email address.")
        if not password:
            raise ValueError("Users must have a password.")
        
        user = self.model(username = username, email = self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(username = username, email = self.normalize_email(email), password = password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def had_module_perms(self, app_label):
        return True


class Project(models.Model):
    name = models.CharField(max_length=64)
    
    def total_hours(self):
        items = self.log_project.all().aggregate(Sum('hours'))
        total = 0 
        if items['hours__sum'] != None :
            total = items['hours__sum']
        return total

    def __str__(self):
        return self.name


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=SET_NULL, null=True, blank=True ,related_name='log_project')
    remarks = models.TextField()
    hours = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()