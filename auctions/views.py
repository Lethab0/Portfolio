# Import necessary modules and components
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Max
from auctions.forms import *
from .models import *


# Main page displaying all listings
def index(request):
    # Retrieve all listings
    listing_object = Auction_listing.objects.all() 
    return render(request, "auctions/shop.html", {"listings": listing_object})


# User login view
def login_view(request):
    if request.method == "POST":
        # Attempt to authenticate user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


# User logout view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


# User registration view
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


# Creating a new listing
@login_required
def Create_listing(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            title = form.cleaned_data["Title"]
            Description = form.cleaned_data["Description"]
            price = form.cleaned_data["current_price"]
            url = form.cleaned_data["Image_url"]
            
            # Create new listing object
            created_listing = Auction_listing(Title=title, Description=Description, current_price=price, Image_url=url, Seller=request.user)
            created_listing.save()

            # Add to categories
            listing = Auction_listing.objects.get(Title=title, Description=Description, current_price=price, Image_url=url, Seller=request.user)
            item_select = request.POST.get('Item_category')  # Selected category
            category_options = Category.objects.get(Heading=item_select)
            category_options.Items.add(listing)
            category_options.save()

        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        category_options = Category.objects.all()  # Get all categories
        Form = PostForm()
        return render(request, "auctions/create.html", {"form": Form, "Categories": category_options})
                
# View for individual listings
@login_required
def Specific_listing(request, ID):
    # Retrieve listing and related data
    creator = Auction_listing.objects.get(id=ID)
    Item = Auction_listing.objects.get(id=ID)
    if (creator.Seller == request.user) and (Bids.objects.filter(Bid_item=Item, State=True).exists()):
        button = 'Close Auction'
    else:
        button = None
        highest_bid = Bids.objects.filter(Bid_item=Item).aggregate(Max('highest_amount'))
        best_bid = highest_bid['highest_amount__max']
    try:
        highest_bidder = Bids.objects.get(Bid_item=Item, highest_amount=best_bid)
    except:
        highest_bidder = None
    
    Comments = Listing_Comments.objects.filter(Comment_item=Item)
    if Bids.objects.filter(Bid_item=ID).exists():
        pass

    # Check the user's watchlist for the item
    if Watchlist.objects.filter(Person_watching=request.user, item=ID).exists():
        Watched = 'Remove from watchlist'
    else:
        Watched = 'Add to watchlist'

    # Check if auction is closed and determine if user won or lost
    won = None
    lost = None
    if Item.Auction_open == False:
        the_highest_bid = Item.current_price
        bid_id = Item.id
        exact_bid = get_object_or_404(Bids, id=bid_id)
        if exact_bid.Bidder == request.user:
            won = True
        else:
            lost = True
            
    return render(request, "auctions/Item.html", {"Item": Item, "Comments": Comments, "Watchlist": Watched, "button": button, "won": won, "lost": lost, "user": request.user})


# Add or remove items from watchlist
@login_required
def add_watchlist(request, ID):
    if Watchlist.objects.filter(Person_watching=request.user, item=ID).exists():
        # Delete if the item exists on user's watchlist
        watchlist_item = Watchlist.objects.get(Person_watching=request.user, item=ID)
        watchlist_item.delete()
        return HttpResponseRedirect(reverse("Specific_listing", args=[ID])) 
    else:
        # Add if the item doesn't exist on user's watchlist
        auction_item = Auction_listing.objects.get(id=ID)
        watchlist_item = Watchlist(Person_watching=request.user, item=auction_item)
        watchlist_item.save()
        return HttpResponseRedirect(reverse("Specific_listing", args=[ID]))

# Place bids on items
@login_required
def Place_bid(request, ID):
    if request.method == "POST":
        bid = request.POST["Bid"]
        if bid == '':
            return HttpResponseRedirect(reverse("Specific_listing", args=[ID]))
        else:
            item = Auction_listing.objects.filter(id=ID)
            current_bids = Bids.objects.filter(Bid_item__in=item, highest_amount__gte=bid).count()

            if current_bids == 0:
                item = Auction_listing.objects.get(id=ID)
                new_bid = Bids(Bidder=request.user, highest_amount=bid, State=True) 
                new_bid.save()
                new_bid.Bid_item.add(item)

                # Update current price of item
                item.current_price = bid
                item.save()
                messages.add_message(request, messages.INFO, "Successfully placed bid")
                return HttpResponseRedirect(reverse("Specific_listing", args=[ID]))
            else:
                messages.add_message(request, messages.INFO, "Unsuccessfully placed bid")
                return HttpResponseRedirect(reverse("Specific_listing", args=[ID]))
                   
    else:
        return HttpResponseRedirect(reverse("Specific_listing", args=[ID]))

# Close bids by setting State to false
@login_required
def close_bid(request, ID):
    item = Auction_listing.objects.get(id=ID)
    all_bids = Bids.objects.filter(Bid_item=item).update(State=False) 
    item.Auction_open = False
    item.save()
    return HttpResponseRedirect(reverse("Specific_listing", args=[ID]))


# Display items on user's watchlist
@login_required
def watchlist(request):
    watch_list = Watchlist.objects.filter(Person_watching=request.user)
    return render(request, "auctions/watchlist.html", {"lists": watch_list})    

# Display different categories
def Categories(request):
    Sections = Category.objects.all()
    return render(request, "auctions/categories.html", {"Categories": Sections})

# Add comments for each item
@login_required
def Comment(request, ID):
    if request.method == "POST":
        text = request.POST["Comment_text"]
        the_item = Auction_listing.objects.get(id=ID)
        new_comment = Listing_Comments(Text=text, Comment_item=the_item)
        new_comment.save()
        return HttpResponseRedirect(reverse("Specific_listing", args=[ID]))
    else:
        return HttpResponseRedirect(reverse("Specific_listing", args=[ID]))
    
# Show items in each category
def Category_items(request, Heading):
    category_name = Category.objects.get(Heading=Heading)
    items = category_name.Items.all()
    print(items)
    return render(request, "auctions/categories.html", {"Items": items})


 
