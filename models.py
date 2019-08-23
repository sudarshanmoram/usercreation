from django.db import models
from django.urls import reverse

class userdata(models.Model):
    username=models.CharField(max_length=25,unique=True,blank=False)
    email=models.EmailField(max_length=30,blank=False)
    password=models.CharField(max_length=20,blank=False)

    def __str__(self):
        return self.username



    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})

class Profile(models.Model):
    user=models.OneToOneField(userdata,on_delete=models.CASCADE)
    profile=models.ImageField(default='default.jpg',upload_to='userprofile_pics')

    def __str__(self):
        return f'{self.user.username} profile'
