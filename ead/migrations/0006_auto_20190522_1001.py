# Generated by Django 2.0.8 on 2019-05-22 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ead', '0005_arquivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivo',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
