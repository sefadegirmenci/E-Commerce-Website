from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm

from .models import Auction, Bid, Comment, User, Category
from django import forms


class NewListingForm(ModelForm):
    class Meta:
        model = Auction
        exclude = ['user', 'bid', ]


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.user = user
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
        return render(request, "auctions/register.html")


def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            bid = Bid(user=request.user, amount=form.cleaned_data['starting_bid'])
            bid.save()
            form = form.save(commit=False)
            form.user = request.user
            form.bid = bid
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_listing.html", {
                "categories": Category.objects.all(),
                "form": form,
                "message": "The form is invalid",
            })
    else:
        form = NewListingForm()
        return render(request, "auctions/new_listing.html", {
            "categories": Category.objects.all(),
            "form": form,
        })


def listing(request, id):
    if request.method == "GET":
        listing = Auction.objects.filter(pk=id).first()
        in_watchlist = False
        owner_of_item = False
        if request.user is not None:
            # watchlist = listing.users.filter(pk=request.user.id).first()
            watchlist = request.user.watchlist.filter(pk=id).first()
            if watchlist is not None:
                in_watchlist = True
            if Auction.objects.get(pk=id).user == request.user :
                owner_of_item=True
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "in_watchlist": in_watchlist,
            "owner_of_item": owner_of_item,
        })
    return render(request, "auctions/listing.html")


def add_watchlist(request, id):
    request.user.watchlist.add(id)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def remove_watchlist(request, id):
    request.user.watchlist.remove(id)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def new_bidding(request, id):
    if request.method == "POST":
        new_bid_amount = int(request.POST.get("new-bid"))
        listing = Auction.objects.get(pk=id)
        if new_bid_amount <= listing.bid.amount:
            in_watchlist = False
            watchlist = request.user.watchlist.filter(pk=id).first()
            if watchlist is not None:
                in_watchlist = True
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "in_watchlist": in_watchlist,
                "message": "The bid amount should be greater than the current bid."
            })
        else:
            prev_bid=listing.bid
            bid = Bid(prev_bid.id,request.user,new_bid_amount)
            bid.save()
            return HttpResponseRedirect(reverse("listing", args=(id,)))
    else:
        return HttpResponseRedirect(reverse("listing", args=(id,)))

def new_comment(request,id):
    if request.method == "POST":
        text = request.POST.get("comment")
        auction = Auction.objects.get(pk=id)
        comment = Comment(user=request.user,auction=auction,comment=text)
        comment.save()

    return HttpResponseRedirect(reverse("listing", args=(id,)))