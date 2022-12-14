# Generated by Django 4.1.2 on 2022-12-13 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_category_alter_user_id_comment_bid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='owner',
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL),
        ),
    ]
