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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isActive= models.BooleanField(default=True)
    owner= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="category")
    category= models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="user")
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_listing_image(self):
        return self.imageUrl

    def get_listing_price(self):
        return self.price

    def get_listing_isActive(self):
        return self.isActive

    def get_listing_owner(self):
        return self.owner

    def get_listing_category(self):
        return self.category

    def get_listing_seller(self):
        return self.seller


class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'imageUrl', 'price', 'isActive', 'owner', 'category', 'seller']

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
