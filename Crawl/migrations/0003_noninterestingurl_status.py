# Generated by Django 2.2.12 on 2020-04-30 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crawl', '0002_auto_20200430_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='noninterestingurl',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
