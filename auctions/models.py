from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
    pass







class Category(models.Model):
    categoryName = models.CharField(max_length=50)


    def __str__(self):
        return self.categoryName

    def get_auction_listings(self):
        return AuctionListing.objects.filter(category=self)






# Model 1: Auction Listings
class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    imageUrl = models.CharField(max_length=1000)
    startingBid = models.DecimalField(max_digits=10, decimal_places=2)
    isActive= models.BooleanField(default=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    watchers= models.ManyToManyField(User, blank=True, related_name="watched_listing")

    def __str__(self):
        return self.title

    def get_listing_title(self):
        return self.title

    def get_listing_description(self):
        return self.description

    def get_listing_image(self):
        return self.imageUrl

    def get_listing_startingBid(self):
        return self.startingBid

    def get_listing_isActive(self):
        return self.isActive


    def get_listing_category(self):
        return self.category

    def get_listing_seller(self):
        return self.seller






class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'imageUrl', 'startingBid', 'isActive', 'category', 'seller']


class WatchList(models.Model):
    auction_listing= models.ManyToManyField(AuctionListing, blank=True, related_name="watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return f"{self.user}'s watchlist"




# Model 2: Bids
class Bid(models.Model):
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_date = models.DateTimeField()






# Model 3: Comments
class Comment(models.Model):
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField()
