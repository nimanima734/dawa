# Generated by Django 5.1.6 on 2025-04-20 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Produits', '0006_alter_produits_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='produits',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
