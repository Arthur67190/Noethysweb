# Generated by Django 3.2.23 on 2024-07-25 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0164_auto_20240723_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='activite',
            name='num_decla',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Numéro de déclaration de l'activité"),
        ),
        migrations.AlterField(
            model_name='activite',
            name='public',
            field=models.IntegerField(choices=[(0, 'Parents'), (1, 'Chef/taine'), (2, 'Chef/taine de groupe - Directeur/trice'), (3, 'Délégué(e) Local'), (4, 'Ami(e)'), (5, 'Jeunes'), (6, 'Tous les adultes sauf les parents')], default=5, verbose_name='Public destinataire'),
        ),
    ]