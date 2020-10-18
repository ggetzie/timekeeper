# Generated by Django 3.0.9 on 2020-10-15 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201015_1418'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hours',
            options={'ordering': ['-date', 'project__number'], 'verbose_name': 'Hours', 'verbose_name_plural': 'Hours'},
        ),
        migrations.AlterField(
            model_name='hours',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, verbose_name='quantity'),
        ),
    ]
