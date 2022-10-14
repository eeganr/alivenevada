from django.db import models
from mapbox_location_field.models import LocationField, AddressAutoHiddenField


class Place(models.Model):
    location = LocationField(
        map_attrs={"center": (-116.108583, 38.433739), "zoom": 4.7, "style": "mapbox://styles/mapbox/outdoors-v11"})
    created_at = models.DateTimeField(auto_now_add=True)
    address = AddressAutoHiddenField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)