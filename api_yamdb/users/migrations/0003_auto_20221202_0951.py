# Generated by Django 2.2.16 on 2022-12-02 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20221202_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='codes', to=settings.AUTH_USER_MODEL),
        ),
    ]
