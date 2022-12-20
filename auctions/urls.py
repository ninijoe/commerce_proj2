from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing/", views.create_listing, name='create_listing'),
    path("categories", views.categories, name='categories'),
    path("watchlist/", views.watchlist, name='watchlist'),
    path("category_listings/<int:category_id>", views.category_listings, name='category_listings'),
    path("listing/<int:listing_id>", views.listing, name='listing'),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name='remove_from_watchlist'),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name='add_to_watchlist'),
    path("comment/<int:listing_id>", views.comment, name='comment'),
    path("add_bid/<int:listing_id>", views.add_bid, name='add_bid'),
    path("remove_bid/<int:listing_id>", views.remove_bid, name='remove_bid')

]
