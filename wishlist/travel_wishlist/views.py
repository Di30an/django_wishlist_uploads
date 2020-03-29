from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.
# This is known as templates in MVC

""" If this is a POST request, the user clicked the ADD button
in the form.  Check if the new place is valid, if so, save a new Place
to the database, and redirect to this same page.
This creates a GET request to this same route.

If not a POST route, or Place is not valid, display a page with
a list of places and a form to add a new place.
"""

def place_list(request):
    # POST request. This will add a new place
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save()    # Create a new Place from the form
        if form.is_valid():         # Checks against DB constraints, for example, are required fields present?
            place.save()            # Saves to the database
            return redirect('place_list')   #redirects to GET view with name place_list - which is the same as view

# If not a POST, or the formis not valid, render the page
# with the form to add a new place, and list of places
    places = Place.objects.filter(visited = False).order_by('name')
    new_place_form = NewPlaceForm()
    return render (request, 'travel_wishlist/wishlist.html', { 'places' : places, 'new_place_form': new_place_form})


def places_visited (request):
    visited = Place.objects.filter(visited = True)
    return render( request, 'travel_wishlist/visited.html',{'visited' : visited})

def place_was_visited( request, place_pk) :
    if request.method  == 'POST':  ## Responds to a POST request
        place = get_object_or_404(Place, pk = place_pk)
        place.visited = True    ## Modifies the boolean visited to True
        place.save() ## Saves the changes to visited
    return redirect('place_list')