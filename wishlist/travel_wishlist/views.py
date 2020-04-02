from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
# Create your views here.
# I believe these function as controllers in the MVC schema

""" If this is a POST request, the user clicked the ADD button
in the form.  Check if the new place is valid, if so, save a new Place
to the database, and redirect to this same page.
This creates a GET request to this same route.

If not a POST route, or Place is not valid, display a page with
a list of places and a form to add a new place.
"""
@login_required
def place_list(request):
    # POST request. This will add a new place
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)    # Create a new Place from the form but doesnt save yet
        place.user = request.user
        if form.is_valid():         # associate the place with the logged-in user
            place.save()            # Saves to the database
            return redirect('place_list')   #redirects to GET view with name place_list - which is the same as view

# If not a POST, or the formis not valid, render the page
# with the form to add a new place, and list of places
    places = Place.objects.filter(user= request.user).filter(visited = False).order_by('name') ## filter creates a list ordered by name
    new_place_form = NewPlaceForm()
    return render (request, 'travel_wishlist/wishlist.html', { 'places' : places, 'new_place_form': new_place_form})

@login_required
def places_visited (request):
    visited = Place.objects.filter(user=request.user).filter(visited = True) # Use the filter function to find all where visited = true. Remember this one.
    return render( request, 'travel_wishlist/visited.html',{'visited' : visited})


@login_required
def place_was_visited(request, place_pk) :
    if request.method  == 'POST':  ## Responds to a POST request, updates 
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else: # Responds to a GET request
            return HttpResponseForbidden()
    return redirect('place_list')

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:  # Checks that the user is the same user for the place
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()


@login_required
def place_details(request, place_pk):
    
    place = get_object_or_404(Place, pk=place_pk)

    if place.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST' :
        form = TripReviewForm( request.POST, request.FILES, instance=place)
        # instance is the model object to update with the form data

        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!' )
        else:
            messages.error(request, form.errors ) # Temp error message - future version should improve

        return redirect ('place_details',place_pk = place_pk)

    else:  #GET place details
        if place.visited:
            review_form = TripReviewForm (instance = place)  # Pre-populate with data from this Place instance
            return render( request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form} )
        else:
            return render (request, 'travel_wishlist/place_detail.html', {'place': place } )