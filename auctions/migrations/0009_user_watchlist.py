# Generated by Django 4.0.3 on 2022-03-10 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auction_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='users', to='auctions.auction'),
        ),
    ]