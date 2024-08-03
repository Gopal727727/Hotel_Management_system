from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
import uuid

Gender = (('Male','Male'),('Female','Female'),('Other','Other'))

def user_directory_path(instance,filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" %(instance.user.id,ext)
    return "User{0}/{1}".format(instance.user.id,filename)

class User(AbstractUser):
    full_name = models.CharField(max_length=500)
    username = models.CharField(max_length=500,unique=True)
    email=models.EmailField(unique=True)
    phone = models.CharField(max_length=20,blank=False,null=False)
    gender = models.CharField(max_length=20,choices=Gender , default="Male" )
    otp = models.CharField(max_length = 20 ,blank=True,null=True )

    USERNAME_FIELD = 'email' #uses user email for login
    REQUIRED_FIELDS = ['username'] 
    
    def __str__(self):
        return self.username
    
class profile(models.Model):
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=user_directory_path , default="default.jpg" , blank=True,null=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    full_name = models.CharField(max_length=500)
    phone = models.CharField(max_length=20,blank=False,null=False)
    gender = models.CharField(max_length=20,choices=Gender , default="Male" )
    address = models.CharField(max_length=300,null=True,blank=True)
    verfied = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        else:
            return f"{self.user.username}"

def create_user_profile(sender,instance,created,**kwargs):
    if created:
        profile.objects.create(user=instance)

def saver_user_profile(sender,instance,**kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(saver_user_profile, sender=User)