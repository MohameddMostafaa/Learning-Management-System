# Generated by Django 4.0.3 on 2023-05-06 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_pendingaccounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingaccounts',
            name='emailVerified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='accounttypes',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='registeredgroups',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.registeredgroups')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
