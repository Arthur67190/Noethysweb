# Generated by Django 3.2.9 on 2021-11-29 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_filtreliste_utilisateur'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='afficher_coords',
            field=models.BooleanField(default=True, verbose_name='Afficher les coordonnées de la structure sur le portail.'),
        ),
    ]