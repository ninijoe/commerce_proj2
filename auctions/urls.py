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
    path("category_listings_search", views.category_listings_search, name='category_listings_search'),
    path("listing/<int:listing_id>", views.listing, name='listing'),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name='remove_from_watchlist'),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name='add_to_watchlist'),
    path("comment/<int:listing_id>", views.comment, name='comment'),
    path("add_bid/<int:listing_id>", views.add_bid, name='add_bid'),
    path("terms", views.terms, name='terms'),
    path("about", views.about, name='about'),
    path("close_listing/<int:listing_id>", views.close_listing, name='close_listing'),
    path("me", views.me, name='me'),
    path("sellers", views.sellers, name='sellers'),
    path("settings", views.settings, name='settings'),
    path("notifications", views.notifications, name='notifications'),
    path("delete_listing/<int:listing_id>", views.delete_listing, name='delete_listing'),
    path("index_search", views.index_search, name='index_search'),
    path("categories_search", views.categories_search, name='categories_search'),
    path("watchlist_search", views.watchlist_search, name='watchlist_search'),
    path("me_search", views.me_search, name='me_search'),

]
