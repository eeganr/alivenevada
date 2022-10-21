from django.db import models
from mapbox_location_field.models import LocationField, AddressAutoHiddenField


class Place(models.Model):
    item = models.TextField(blank=True, null=True)
    location = LocationField(
        map_attrs={"center": (-116.108583, 38.433739), "zoom": 4.7, "style": "mapbox://styles/mapbox/outdoors-v11"})
    address = AddressAutoHiddenField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    uuid = models.CharField(max_length=100, blank=True, null=True)