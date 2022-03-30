from ast import Str
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models import Sum

# Create your models here.
class ListedGames(models.Model):
    name = models.CharField(max_length=300)
    theme_image = models.ImageField()
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:game", kwargs={"slug": self.slug})    

    class Meta:
        verbose_name_plural='Listed Games' 

class PostImage(models.Model):
    game_account = models.ForeignKey('GameAccounts', null=True, blank=True, on_delete=models.CASCADE)
    images = models.ImageField()
 
    def __str__(self):
        return str(self.game_account.id) 

class GameAccounts(models.Model):
    description = models.CharField(max_length=300)
    rate = models.PositiveIntegerField()
    game = models.ForeignKey(ListedGames, on_delete=models.CASCADE)
    acc_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    payment_done = models.BooleanField(default=False) 
    ordered = models.BooleanField(default=False) 

    def __str__(self):
        return str(self.id)

    def account_images(self):
        return PostImage.objects.filter(game_account=self.pk)     

     

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    ordered = models.BooleanField(default=False) 
    game_account = models.ForeignKey(GameAccounts, on_delete=models.CASCADE)  
    payment_done = models.BooleanField(default=False) 

    def __str__(self):
        return str(self.game_account.id)

    def total_price_per_account(self):
        return self.game_account.rate    

class CartOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game_accounts = models.ManyToManyField(CartItem)
    cart_created_on = models.DateTimeField(auto_now_add=True)
    account_delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def is_added(self):
        my_list = []
        for acc in self.game_accounts.values():
            my_list.append(acc['game_account_id'])
        return my_list

    def get_total(self):
        total = 0
        for order_item in self.game_accounts.filter(ordered=False):
            total += order_item.total_price_per_account()  
        return total    
   
class Payment(models.Model):
    razorpay_payment_id = models.CharField(max_length=100)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_signature = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.user.username
   


  

   
      

        

