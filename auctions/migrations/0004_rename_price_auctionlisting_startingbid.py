# Generated by Django 4.1.2 on 2022-12-13 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_auctionlisting_owner_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='price',
            new_name='startingBid',
        ),
    ]
