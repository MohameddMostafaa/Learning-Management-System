# Generated by Django 4.0.3 on 2023-05-17 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0011_alter_pendingaccounts_name_alter_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='name',
            new_name='title',
        ),
    ]
