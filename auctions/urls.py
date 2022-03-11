from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing",views.new_listing, name="new-listing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add-watchlist"),
    path("remove_watchlist/<int:id>", views.remove_watchlist, name="remove-watchlist"),
    path("new_bidding/<int:id>", views.new_bidding, name="new-bidding"),
    path("new_comment/<int:id>", views.new_comment, name="new-comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("<str:id>/categories", views.specific_category, name="specific-category"),
]
