# Generated by Django 4.0.3 on 2023-05-19 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0014_alter_posts_cansubmit_submissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='file',
            field=models.FileField(null=True, upload_to='documents/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='file',
            field=models.FileField(null=True, upload_to='documents/%Y/%m/%d'),
        ),
    ]