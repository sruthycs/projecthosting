# Generated by Django 4.1 on 2023-03-30 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dairyapp', '0002_reviewrating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='review',
        ),
    ]
