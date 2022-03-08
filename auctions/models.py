from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

class Auction(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=1024)
    starting_bid = models.IntegerField()
    category = models.ManyToManyField(Category, blank= True,related_name="categories_auction")
    url = models.CharField(max_length=128)
    def __str__(self):
        return f"{self.user.name}: {self.title}"

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE,related_name="auctions_bid")
    amount = models.IntegerField()
    def __str__(self):
        return f"{self.user.name} {self.auction.title}: {self.amount}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE,related_name="auctions_comment")
    comment = models.TextField(max_length=1024)
    def __str__(self):
        return f"{self.user.name} {self.auction.title}: {self.comment}"