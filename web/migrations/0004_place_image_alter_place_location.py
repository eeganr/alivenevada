# Generated by Django 4.1.2 on 2022-10-14 05:24

from django.db import migrations, models
import mapbox_location_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_place_delete_somelocationmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='place',
            name='location',
            field=mapbox_location_field.models.LocationField(map_attrs={'center': (-116.108583, 38.433739), 'style': 'mapbox://styles/mapbox/outdoors-v11', 'zoom': 4.7}),
        ),
    ]
