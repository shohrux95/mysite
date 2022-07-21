from distutils.command.upload import upload
from django.db import models
from django.forms import SlugField
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=250)
    product_type=models.CharField(max_length=25)
    product_description=models.TextField()
    affiliate_url=models.SlugField(blank=True,null=True)
    image=models.ImageField(upload_to='product')
    product_price=models.IntegerField()

    def discount(self):
        if self.discount_percent > 0:
            discounted_price = self.price - self.price * self.discount_percent / 100
            return discounted_price
    def price(self):
        summ=0
        objects=self.product_price.all()
        for sum in objects:
            summ+=sum
        return summ

    def __str__(self) -> str:
        return self.product_name

    def price(self):
        return     
class Tag(models.Model):
    tag_name=models.CharField(max_length=150)
    tag_slug=models.SlugField()

    def __str__(self) -> str:
        return self.tag_name

class Article(models.Model):
    article_title=models.CharField(max_length=150)
    article_published=models.DateTimeField('date published')
    article_image=models.ImageField(upload_to='article')
    article_tags=models.ManyToManyField(Tag)
    atricle_content=HTMLField()
    article_slug=models.SlugField()



    def __str__(self) -> str:
        return self.article_title

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    product=models.ManyToManyField(Product)

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,*args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save,sender=User)
def save_user_profile(sender,instance,created, *args, **kwargs):
    instance.profile.save()        

