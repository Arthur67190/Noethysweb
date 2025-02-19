# Generated by Django 3.2.23 on 2024-07-23 13:22

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0162_merge_0158_auto_20240718_1243_0161_structure_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='individu',
            name='statut',
            field=models.IntegerField(blank=True, choices=[(0, 'Parent'), (1, 'Chef/taine'), (2, 'Chef/taine de groupe - Directeur/trice'), (3, 'Délégué(e) Local'), (4, 'Ami(e)')], default=0, null=True, verbose_name='Situation des parents'),
        ),
        migrations.AlterField(
            model_name='rattachement',
            name='categorie',
            field=models.IntegerField(choices=[(1, 'Adulte'), (2, 'Enfant'), (3, 'Contact')], db_column='Catégorie', default=1),
        ),
        migrations.AlterField(
            model_name='sondage',
            name='categories_rattachements',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Adulte'), (2, 'Enfant'), (3, 'Contact')], help_text="Sélectionnez les catégories d'individus qui pourront être associés à ce formulaire.", max_length=200, null=True, verbose_name='Catégories de rattachement'),
        ),
    ]
