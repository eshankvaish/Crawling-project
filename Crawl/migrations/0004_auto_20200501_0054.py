# Generated by Django 2.2.12 on 2020-04-30 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Crawl', '0003_noninterestingurl_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitedata',
            name='add_base_url',
        ),
        migrations.RemoveField(
            model_name='sitedata',
            name='site_regex',
        ),
    ]
