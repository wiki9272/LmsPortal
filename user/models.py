from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyUserManager(BaseUserManager):
    def create_user(self, email, name,role,developer_type='none', password=None):
        if not email:
            raise ValueError("Users must have an email address")
        dev_type = 'none'
        if role == 'developer':
            dev_type = developer_type
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            role=role,
            developer_type = dev_type
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
            developer_type='none'
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
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    developer_type = models.CharField(max_length=20, choices=DEV_CHOICES, default='None')

    
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


# class Developer(models.Model):
#     ROLE_CHOICES = (
#         ('frontend', 'Frontend'),
#         ('backend', 'Backend'),
#         ('qa','QA')
#     )
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='developer_profile')
#     assigned_projects = models.ManyToManyField('Project', related_name='projects', blank=True)
    
#     def __str__(self):
#         return "Developer: {self.user.username}"
    
#     # Project model
# class Project(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     deadline = models.DateField(),
#     assigned_to = models.ManyToManyField('Developer',related_name='developers', blank=True)

#     def __str__(self):
#         return self.name
    
