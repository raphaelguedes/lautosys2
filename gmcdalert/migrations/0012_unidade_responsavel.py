# Generated by Django 2.0.8 on 2019-05-21 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gmcdalert', '0011_alerta'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidade',
            name='responsavel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gmcdalert.Responsavel'),
        ),
    ]
