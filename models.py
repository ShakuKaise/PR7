from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models


# User Manager
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Role Model
class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Custom User
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set_permissions')

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_role(self):
        return self.role.name if self.role else "No Role"


# Language Model
class Language(models.Model):
    name = models.CharField(max_length=30)
    chars_code = models.CharField(max_length=5)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Publishers Model
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=30)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Author Model
class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Book Model
class Book(models.Model):
    name = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    cover_url = models.URLField()
    quantity = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    publishers = models.ManyToManyField(Publisher, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    authors = models.ManyToManyField(Author, blank=True)

    def __str__(self):
        return self.name

class RequestStatus(models.TextChoices):
    RENTED = 'RENTED'
    EXPIRED = 'EXPIRED'
    RETURNED = 'RETURNED'
    PENDING = 'PENDING'


# Request Model
class Request(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=RequestStatus.choices)

    def __str__(self):
        return f"Request #{self.id} - {self.user} - {self.book} - {self.status}"

# Comment Model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    is_deleted = models.BooleanField(default=False)


# Evaluation Model
class Evaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    evaluation = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
