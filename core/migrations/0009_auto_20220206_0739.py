# Generated by Django 3.2.12 on 2022-02-06 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_cartorder_game_accounts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartorder',
            old_name='start_date',
            new_name='cart_created_on',
        ),
        migrations.RemoveField(
            model_name='cartorder',
            name='ordered_date',
        ),
    ]
