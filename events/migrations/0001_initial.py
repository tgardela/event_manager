# Generated by Django 4.2.2 on 2023-06-29 08:07

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
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('capacity', models.IntegerField()),
                ('attendees', models.ManyToManyField(blank=True, related_name='attendees', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
