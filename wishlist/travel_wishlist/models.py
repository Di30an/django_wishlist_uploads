from django.db import models

# Create your models here.
# This describes a Place table in the database

class Place(models.Model):
    name = models.CharField(max_length = 200)
    visited = models.BooleanField( default = False)
    # Creates a string method that will attributes of the model
    def __str__(self):
        return f'{self.name}, visted? {self.visited}'