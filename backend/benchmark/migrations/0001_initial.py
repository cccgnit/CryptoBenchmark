# Generated by Django 3.0.3 on 2020-05-03 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CipherResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cipher', models.CharField(max_length=100)),
                ('startTime', models.IntegerField()),
                ('elapsedTime', models.FloatField()),
                ('throughput', models.FloatField()),
                ('cpuUtilPct', models.FloatField(blank=True, null=True)),
                ('memUsed', models.FloatField(blank=True, null=True)),
                ('memUsedPct', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
