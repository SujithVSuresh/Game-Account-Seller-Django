# Generated by Django 3.2.12 on 2022-02-25 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_postimage_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='game_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.gameaccounts'),
        ),
    ]