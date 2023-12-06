from django.db import models
from django.db.models.signals import post_save
from .signals import newsletter_post_save
# Create your models here.

def upload_to(instance, filename):
    return '/'.join(['images', str(instance.id), filename])


class NewsletterModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    desc = models.TextField(max_length=500,blank=True,null=True)
    img = models.ImageField(upload_to=upload_to,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class NewsletterSubscriber(models.Model):

    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


post_save.connect(newsletter_post_save,sender=NewsletterModel)