# Generated by Django 4.1.2 on 2022-10-20 03:07

from django.db import migrations, models
import mapbox_location_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.TextField(blank=True, null=True)),
                ('location', mapbox_location_field.models.LocationField(map_attrs={'center': (-116.108583, 38.433739), 'style': 'mapbox://styles/mapbox/outdoors-v11', 'zoom': 4.7})),
                ('address', mapbox_location_field.models.AddressAutoHiddenField(map_id='map')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('uuid', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]