# Generated by Django 2.0.8 on 2019-06-13 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas_a_pagar', '0002_auto_20190613_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='observacao',
            field=models.TextField(blank=True, null=True),
        ),
    ]
