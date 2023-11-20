from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):

    def create_user(self, email, name, password=None, status=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, status=status)

        # print(user)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password=None, status=None):
        user = self.create_user(email, name, password, status)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user
    

class UserAccount(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name
    
    def __str__(self):
        return self.email


class Video(models.Model):
    name = models.CharField(max_length=255)
    transcript = models.TextField()


class Summary(models.Model):
    name = models.CharField(max_length=255)
    summary = models.TextField()

