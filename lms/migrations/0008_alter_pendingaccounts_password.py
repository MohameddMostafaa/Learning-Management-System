# Generated by Django 4.0.3 on 2023-05-16 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0007_alter_courses_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingaccounts',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]
