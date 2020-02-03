from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=15, verbose_name="First name", blank=True)
    last_name = models.CharField(max_length=15, verbose_name="Last name", blank=True)
    avatar = models.ImageField(verbose_name="avatar", blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    @property
    def is_staff(self):
        return self.is_admin

class Product(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = "Product"
        verbose_name_plural = "Products"

    name = models.CharField(max_length=50, verbose_name="Name")
    year = models.IntegerField(verbose_name="Year")
    color = models.CharField(max_length=7, verbose_name="Color")
    pantone_value = models.CharField(max_length=15,
                                     verbose_name="Pantone value")
