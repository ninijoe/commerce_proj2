from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.middleware import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import User, Category, AuctionListing, AuctionListingForm, WatchList




def index(request):
    listings = AuctionListing.objects.filter(isActive=True)
    return render(request, 'auctions/index.html', {'listings': listings})





def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {'categories': categories})





def listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    context = {
        'title': listing.get_listing_title(),
        'description': listing.get_listing_description(),
        'imageUrl': listing.get_listing_image(),
        'startingBid': listing.get_listing_startingBid(),
        'isActive': listing.get_listing_isActive(),
        'category': listing.get_listing_category(),
        'seller': listing.get_listing_seller(),

    }
    return render(request, 'auctions/listing.html', context)






@login_required(login_url='login')
def watchlist(request):
    listing = AuctionListing.objects.filter(watchers= request.user)
    watchlist= WatchList.objects.filter(user= request.user)
    return render(request, 'auctions/watchlist.html', {'watchlist': watchlist, 'listing': listing})










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
def add_to_watchlist(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        user = request.user

        try:
            listing = AuctionListing.objects.get(id=listing_id)

            # check if the listing is already in the watchlist
            if Watchlist.objects.filter(user=user, listing=listing).exists():
                context = {
                    'message': 'listing exist in watchlist already'
                }
                return render(request, 'auctions/watchlist.html', context)
            else:
                watchlist, created = Watchlist.objects.create(user=user, listing=listing)
                context = {
                    'message': 'listing added successfully',
                    'watchlist': watchlist
                }
                return render(request, 'auctions/watchlist.html', context)
        except ValueError:
            return redirect('watchlist')



@login_required(login_url='login')
def remove_from_watchlist(request ):
    return





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
