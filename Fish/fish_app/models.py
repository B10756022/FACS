from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# 辨識魚隻模組
class Video(models.Model):
    caption=models.CharField(max_length=100)
    video=models.FileField(upload_to="video/")
    after_predict =models.FileField(upload_to='predict_video/',blank=True)
    quantity = models.IntegerField(blank=False, default=0)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.caption


# 個人資料
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nonce = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# 顧客
class Customer(models.Model):
    name = models.CharField(max_length=10, blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    location = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

# 訂單
class Order(models.Model):
    price = models.IntegerField(blank=False, default=0) #價格
    quantity = models.IntegerField(blank=False, default=0) #數量
    place = models.CharField(max_length=20) #市場
    fish_species = models.CharField(max_length=10) #魚種
    date = models.DateField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.user)+"訂單，"+str(self.place)+ "市場" + self.fish_species + str(self.quantity)+"隻"
