from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django.conf import settings

class CustomUser(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    url = models.URLField()
    date = models.DateTimeField()
    domain = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
    users_added = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='articles_to_read', blank=True)

    def __str__(self):
        return self.title

class CoinAmount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coin_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=19, decimal_places=8)
    price_usd = models.DecimalField(max_digits=19, decimal_places=8)
    change_percent_24hr = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s {self.coin_id} Amount"
