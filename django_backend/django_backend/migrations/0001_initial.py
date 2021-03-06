# Generated by Django 3.2.4 on 2021-06-16 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Characteristics',
            fields=[
                ('characteristic_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='GarmentWomen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_path', models.CharField(max_length=100)),
                ('count_for_each_ranking', models.JSONField(default={'rank_1': 0, 'rank_10': 0, 'rank_2': 0, 'rank_3': 0, 'rank_4': 0, 'rank_5': 0, 'rank_6': 0, 'rank_7': 0, 'rank_8': 0, 'rank_9': 0})),
                ('characteristics', models.ManyToManyField(to='django_backend.Characteristics')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GarmentOthers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_path', models.CharField(max_length=100)),
                ('count_for_each_ranking', models.JSONField(default={'rank_1': 0, 'rank_10': 0, 'rank_2': 0, 'rank_3': 0, 'rank_4': 0, 'rank_5': 0, 'rank_6': 0, 'rank_7': 0, 'rank_8': 0, 'rank_9': 0})),
                ('garment_type', models.CharField(choices=[('U', 'Unisex'), (None, 'Unknown')], max_length=100)),
                ('characteristics', models.ManyToManyField(to='django_backend.Characteristics')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GarmentMen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_path', models.CharField(max_length=100)),
                ('count_for_each_ranking', models.JSONField(default={'rank_1': 0, 'rank_10': 0, 'rank_2': 0, 'rank_3': 0, 'rank_4': 0, 'rank_5': 0, 'rank_6': 0, 'rank_7': 0, 'rank_8': 0, 'rank_9': 0})),
                ('characteristics', models.ManyToManyField(to='django_backend.Characteristics')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
