from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
import datetime
from django.utils import timezone



class User(AbstractUser):
    pass





class Category(models.Model):
    categoryName = models.CharField(max_length=50)



    def __str__(self):
        return self.categoryName

    def get_auction_listings(self):
        return AuctionListing.objects.filter(category=self)







class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    imageUrl = models.CharField(max_length=1000)
    startingBid = models.DecimalField(max_digits=10, decimal_places=2)
    isActive= models.BooleanField(default=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank = True, related_name= "watchlist" )
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name="seller")
    created = models.DateTimeField(default = timezone.now)

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

    def get_listing_watchlist(self):
        return f"{self.seller_id}'s watchlist "


    def get_listing_seller_id(self):
        return f" {self.title} posted by {self.seller_id} "


    def created(self):
        return self.created





class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'imageUrl', 'startingBid', 'isActive', 'category']











class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="bidder", default=None)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=True, related_name="listing", default=None)

    def __str__(self):
        return f" {self.bidder} made a bid of {self.bid} on {self.auction_listing} "










class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']







class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="author", default=None)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=True, related_name="auction_listing")
    comment = models.TextField(max_length=200 , default=None)
    created = models.DateTimeField(default = datetime.datetime.now)


    def __str__(self):
        return f" on {self.created}, {self.author} dropped a comment on {self.auction_listing} "
