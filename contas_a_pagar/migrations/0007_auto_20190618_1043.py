# Generated by Django 2.0.8 on 2019-06-18 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contas_a_pagar', '0006_conta_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='remetente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remetente', to='lauto.User2'),
        ),
    ]
