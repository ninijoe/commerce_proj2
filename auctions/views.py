from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.middleware import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages


from .models import User, Category, Bid, AuctionListing, AuctionListingForm, Comment, Bid , BidForm




def index(request):
    listings = AuctionListing.objects.filter(isActive=True)
    return render(request, 'auctions/index.html', {'listings': listings})





def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {'categories': categories})





def listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)

    isListingInWatchList = request.user in listing.watchlist.all()

    all_Comments = Comment.objects.filter(auction_listing = listing)


    context = {
        'title': listing.get_listing_title(),
        'description': listing.get_listing_description(),
        'imageUrl': listing.get_listing_image(),
        'startingBid': listing.get_listing_startingBid(),
        'isActive': listing.get_listing_isActive(),
        'category': listing.get_listing_category(),
        'isListingInWatchList': isListingInWatchList,
        'listing_id': listing_id,
        'listing': listing,
        'all_Comments': all_Comments,


    }
    return render(request, 'auctions/listing.html', context)






@login_required(login_url='login')
def add_bid(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['bid']
            if bid >= listing.startingBid:
                try:
                    float(bid)
                    listing.startingBid = bid
                    listing.save()
                    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

                except ValueError:
                    raise ValueError("Bid amount must be an integer or floating point number ").format(user)

            else:
                messages.error(request, "Bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any).")
                return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
    else:
        form = BidForm()

    context = {
        'title': listing.get_listing_title(),
        'description': listing.get_listing_description(),
        'imageUrl': listing.get_listing_image(),
        'startingBid': listing.get_listing_startingBid(),
        'isActive': listing.get_listing_isActive(),
        'category': listing.get_listing_category(),
        'listing_id': listing_id,
        'listing': listing,
        'form': form
    }

    return render(request, 'auctions/listing.html', context)







def create_listing(request):
    #Checks if the request method is a POST request
    if request.method == 'POST':
        #Creates an AuctionListingForm object with the POST data
        form = AuctionListingForm(request.POST)
        #Checks if the form is valid
        if form.is_valid():
            #Sets the user of the listing to the current user
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        #If the request method is not a POST request, creates an empty AuctionListingForm object
        form = AuctionListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})







def category_listings(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = AuctionListing.objects.filter(category=category)
    return render(request, 'auctions/category_listings.html', {'listings': listings, 'category': category})










@login_required(login_url='login')
def watchlist(request):
    user = request.user
    listings = user.watchlist.all()
    context = {
        'listings': listings
    }
    return render(request, 'auctions/watchlist.html', context)












@login_required(login_url='login')
def add_to_watchlist(request , listing_id ):
    listing = AuctionListing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))








@login_required(login_url='login')
def remove_from_watchlist(request , listing_id ):
    listing = AuctionListing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))







@login_required(login_url='login')
def comment(request , listing_id ):

    try:
        user = request.user
        listing = AuctionListing.objects.get(pk=listing_id)
        message = request.POST.get('comment')

        comment = Comment (
            author = user,
            auction_listing = listing,
            comment = message,


        )
        comment.save()
    except ValueError:
        raise ValueError("You are seeing this error because you have attempted to make a comment. For security purposes, Guest accounts are prohibited from making comments. Log in or create an account to make a comment".format(user))

    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))





def login_view(request):

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:

        return render(request, "auctions/login.html", {'csrf_token': csrf.get_token(request)})









def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))






def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {'csrf_token': csrf.get_token(request)})
