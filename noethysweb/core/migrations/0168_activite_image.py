# Generated by Django 3.2.23 on 2024-08-07 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0167_alter_reglement_modelimp'),
    ]

    operations = [
        migrations.AddField(
            model_name='activite',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='activite_images/', verbose_name="Image de l'activité"),
        ),
    ]