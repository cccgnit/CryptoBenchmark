# Generated by Django 3.0.3 on 2020-05-14 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benchmark', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.IntegerField(blank=True, null=True)),
                ('cpuUtilPct', models.FloatField(blank=True, null=True)),
                ('memUsedPct', models.FloatField(blank=True, null=True)),
                ('getTotal', models.IntegerField(blank=True, null=True)),
                ('sentTotal', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
