# Generated by Django 3.2.23 on 2025-06-03 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0196_alter_activite_maitrise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typepiece',
            name='public',
            field=models.CharField(choices=[('individu', 'Individu')], max_length=50, verbose_name='Public'),
        ),
    ]
