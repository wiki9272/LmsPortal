from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.timezone import now

class MyUserManager(BaseUserManager):
    def create_user(self, email, name,role,job='none', password=None):
        if not email:
            raise ValueError("Users must have an email address")
        dev_type = 'none'
        if role == 'developer':
            dev_type = job
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            role=role,
            job = dev_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, name,role, password=None):
        user = self.create_user(
            email,
            name=name,
            role=role,
            password=password,
            job='none'
        )
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('developer', 'Developer'),
        ('lead', 'Lead'),
        ('admin','Admin')
    )
    DEV_CHOICES =(
        ('front-end','FrontEnd'),
        ('back-end','BackEnd'),
        ('qa','QA'),
        ('none','None')
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='developer')
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
        primary_key=True
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    job = models.CharField(max_length=20, choices=DEV_CHOICES, default='None')

    
    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","role"]

    def __str__(self):
        return self.email

    @property
    def is_developer(self):
        return self.role == 'developer'
    @property
    def is_lead(self):
        return self.role == 'lead'
    @property
    def is_admin(self):
        return self.role == 'admin'
    @property
    def is_staff(self):
        return self.role == 'admin'
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
        primary_key=True
    )
    details = models.TextField()

class Project(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('in progress','In Progress'),
    )
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client', null=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    deadline = models.DateTimeField(null=True, blank=True)
    assigned_on = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ManyToManyField(User,related_name='project', blank=True, limit_choices_to={'role':'developer'})
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_by", limit_choices_to={'role':'lead'})

    def __str__(self):
        return self.name

class Task(models.Model):
    FLAG_CHOICES = (
        ('red', 'Red'),
        ('yellow', 'Yellow'),
        ('green','Green'),
        ('none','None'),
    )
    project_name = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='task',blank=True)
    name = models.CharField(max_length=255)
    details = models.TextField()
    flag = models.CharField(max_length=20, choices=FLAG_CHOICES, default='none')
    time_to_complete = models.DateTimeField(null=True, blank=True)
    time_taken = models.IntegerField(default=0, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', limit_choices_to={'role':'developer'})
    isCompleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    