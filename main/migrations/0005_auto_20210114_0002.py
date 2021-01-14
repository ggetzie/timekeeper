# Generated by Django 3.0.9 on 2021-01-14 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20201015_1509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name'], 'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AddField(
            model_name='project',
            name='total_hours',
            field=models.IntegerField(default=-1, verbose_name='Total Hours'),
        ),
    ]
