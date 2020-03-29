from django.urls import path
from . import views
"""
Remember that pages like wish list, which shows a list and also accepts
both GET and POST request.
GET request, show form and list of places
POST request, add new place to DB then redirects to a list of places

"""

urlpatterns = [
    path ('',views.place_list, name='place_list'),
    path ('visited', views.places_visited, name = 'places_visited'),
    path ('place/<int:place_pk>/was_visited/', views.place_was_visited, name='place_was_visited')
    
]