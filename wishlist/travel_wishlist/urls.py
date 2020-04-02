from django.urls import path
from . import views
"""
Remember that pages like wish list, which shows a list and also accepts
both GET and POST request.
GET request, show form and list of places
POST request, add new place to DB then redirects to a list of places

"""

urlpatterns = [
    path('',views.place_list, name='place_list'),  # Make sure to add commas next to each path.
    path('visited', views.places_visited, name = 'places_visited'), # name refers to the url path 
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'), ## Created for the "Visited!" button
    path('place/<int:place_pk>', views.place_details, name ='place_details'),
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place'),
]