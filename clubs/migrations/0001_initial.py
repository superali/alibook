# Generated by Django 2.1 on 2019-02-22 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('content', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('approved', models.BooleanField(default=True)),
                ('admins', models.ManyToManyField(blank=True, related_name='admin', to=settings.AUTH_USER_MODEL)),
                ('joined', models.ManyToManyField(blank=True, related_name='joingroup', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clubs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='JoinRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete='CASCADE', related_name='group', to='clubs.Group')),
                ('user', models.ForeignKey(on_delete='CASCADE', related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
