# Generated by Django 2.2.5 on 2019-09-26 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patios', '0002_auto_20190925_1600'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'ordering': ['-fecha_solicitud']},
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(max_length=16),
        ),
    ]
