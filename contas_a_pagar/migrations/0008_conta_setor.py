# Generated by Django 2.0.8 on 2019-06-25 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lauto', '0013_auto_20190612_1539'),
        ('contas_a_pagar', '0007_auto_20190618_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='conta',
            name='setor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lauto.Setor'),
        ),
    ]
