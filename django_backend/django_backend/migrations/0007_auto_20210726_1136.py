# Generated by Django 3.2.4 on 2021-07-26 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_backend', '0006_auto_20210722_1729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='garmentmen',
            old_name='combined_count_for_each_ranking',
            new_name='count_for_each_ranking',
        ),
        migrations.RenameField(
            model_name='garmentmen',
            old_name='combined_score',
            new_name='score',
        ),
        migrations.RenameField(
            model_name='garmentothers',
            old_name='combined_count_for_each_ranking',
            new_name='count_for_each_ranking',
        ),
        migrations.RenameField(
            model_name='garmentothers',
            old_name='combined_score',
            new_name='score',
        ),
        migrations.RenameField(
            model_name='garmentwomen',
            old_name='combined_count_for_each_ranking',
            new_name='count_for_each_ranking',
        ),
        migrations.RenameField(
            model_name='garmentwomen',
            old_name='combined_score',
            new_name='score',
        ),
    ]
