# Generated by Django 3.0.3 on 2020-03-02 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diputados', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comision',
            options={'verbose_name': 'Comisión/Comité', 'verbose_name_plural': 'Comisiones y Comités'},
        ),
        migrations.AddField(
            model_name='distrito',
            name='status',
            field=models.IntegerField(choices=[(1, 'Activo'), (2, 'Inactivo')], default=1, verbose_name='Estado'),
        ),
    ]
