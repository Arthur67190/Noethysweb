# Generated by Django 3.2.23 on 2024-04-22 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0154_auto_20240416_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscription',
            name='tarifs',
            field=models.ManyToManyField(blank=True, default=1, to='core.Tarif', verbose_name='Tarifs'),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='categorie_tarif',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.categorietarif', verbose_name='Catégorie de tarif'),
        ),
    ]